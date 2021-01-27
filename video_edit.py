import os

import moviepy.editor as mvpy
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.drawing import blit
from moviepy.video.tools.segmenting import findObjects
from moviepy.video.fx.mask_color import mask_color

import numpy as np

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets


def fix_problem_pos_mlt_clips(self, picture, t):
    """
    Временное решение проблемы Multiple ImageClips
    """
    hf, wf = framesize = picture.shape[:2]

    if self.ismask and picture.max():
        return np.minimum(1, picture + self.blit_on(np.zeros(framesize), t))
    # -----------------------
    if self.start == 6:  # t_sets['start']
        ct = t + 7 - self.start  # clip time
    # -----------------------
    else:
        ct = t - self.start  # clip time

    img = self.get_frame(ct)
    mask = self.mask.get_frame(ct) if self.mask else None

    if mask is not None and ((img.shape[0] != mask.shape[0]) or (img.shape[1] != mask.shape[1])):
        img = self.fill_array(img, mask.shape)

    hi, wi = img.shape[:2]

    # SET POSITION
    pos = self.pos(ct)

    # preprocess short writings of the position
    if isinstance(pos, str):
        pos = {'center': ['center', 'center'],
               'left': ['left', 'center'],
               'right': ['right', 'center'],
               'top': ['center', 'top'],
               'bottom': ['center', 'bottom']}[pos]
    else:
        pos = list(pos)

    # is the position relative (given in % of the clip's size) ?
    if self.relative_pos:
        for i, dim in enumerate([wf, hf]):
            if not isinstance(pos[i], str):
                pos[i] = dim * pos[i]

    if isinstance(pos[0], str):
        D = {'left': 0, 'center': (wf - wi) / 2, 'right': wf - wi}
        pos[0] = D[pos[0]]

    if isinstance(pos[1], str):
        D = {'top': 0, 'center': (hf - hi) / 2, 'bottom': hf - hi}
        pos[1] = D[pos[1]]

    pos = map(int, pos)

    return blit(img, picture, pos, mask=mask, ismask=self.ismask)


class TrickyBugImg(mvpy.ImageClip):

    def blit_on(self, picture, t):
        """
        Returns the result of the blit of the clip's frame at time `t`
        on the given `picture`, the position of the clip being given
        by the clip's ``pos`` attribute. Meant for compositing.
        """
        return fix_problem_pos_mlt_clips(self, picture, t)


class TrickyBugText(mvpy.TextClip):

    def blit_on(self, picture, t):
        """
        Returns the result of the blit of the clip's frame at time `t`
        on the given `picture`, the position of the clip being given
        by the clip's ``pos`` attribute. Meant for compositing.
        """
        return fix_problem_pos_mlt_clips(self, picture, t)


def edit_video(loadtitle, savetitle, cuts):
    """
    Main function. Сценарий обработки видео.
    :param loadtitle: указатель на видео, имя
        :type loadtitle: str
    :param savetitle: имя для обработанного видео
        :type savetitle: str
    :param cuts: список временных меток для обрезки видео
        :type cuts: list(tuple[t, t]), t is hh:mm:ss.ms
    :return: None
    """
    video = mvpy.VideoFileClip(loadtitle, target_resolution=(1080, 1920))
    im = mvpy.ImageClip('files/icon/window.png')
    regions = findObjects(im)

    back_clips = [mvpy.VideoFileClip('media/load/IMG_0833.MP4', audio=False).subclip(12, 22)]
    comp_clips = [c.resize(r.size)
                  .set_mask(r.mask)
                  .set_pos(r.screenpos)
                  for c, r in zip([back_clips[0], back_clips[0]], [regions[1], regions[2]])]

    clips = []
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        clips.append(clip)

    final_clip = mvpy.concatenate_videoclips(clips)

    text_1 = edit_text("Moscow River", 'text_1')
    text_2 = edit_text("Moscow City", 'text_2')

    logo_1 = add_img("files/icon/location.png", mark='text_1')
    logo_2 = add_img("files/icon/location.png", mark='text_2')

    # masked_logo_1 = mask_color(logo_1, color=[255, 255, 255])
    # masked_logo_2 = mask_color(logo_2, color=[255, 255, 255], thr=20, s=3)

    final_clip = mvpy.CompositeVideoClip([final_clip,
                                          text_1, text_2,
                                          logo_1, logo_2,
                                          *comp_clips], use_bgclip=True)  # use_bgclip=True

    save_video(final_clip, savetitle)
    video.close()


def add_img(img, mark):
    logo = TrickyBugImg(img)

    traj = Trajectory.load_list(t_sets[mark]['tracking'])
    for i in traj[1:]:
        logo = logo.set_position(i)

    logo = logo.set_start(t_sets[mark]['start'])
    logo = logo.set_end(t_sets[mark]['end'])
    logo = logo.crossfadein(t_sets[mark]['fadein'])
    # logo = logo.crossfadein(t_sets[mark]['fadeout'])

    return logo


def edit_text(text, mark):
    """
    Добавление титров
    :param text: текст
        :type text: str
    :param mark: указатель на настройки титров (для settings)
        :type mark: str
    :return: TextClip
    """
    text = TrickyBugText(text,
                         font=t_sets[mark]['font'],
                         fontsize=t_sets[mark]['fontsize'],
                         color=t_sets[mark]['color'],
                         stroke_color='grey'
                         # bg_color=t_sets[mark]['bg_clr']
                         )

    traj = Trajectory.load_list(t_sets[mark]['tracking'])
    for i in traj[:1]:
        text = text.set_position(i)

    text = text.set_start(t_sets[mark]['start'])
    text = text.set_end(t_sets[mark]['end'])
    text = text.crossfadein(t_sets[mark]['fadein'])
    # text = text.crossfadein(t_sets[mark]['fadeout'])

    return text


def save_video(clip, savetitle, path='media/save'):
    """
    Сохранение готового видео
    :param clip: обработанное видео
        :type clip: moviepy.editor.VideoClip
    :param savetitle: имя видео
        :type savetitle: str
    :param path: путь сохраненного видео
        :type path: str
    :return: None
    """
    path = os.path.join(path)
    os.makedirs(path, exist_ok=True)

    clip.write_videofile(savetitle, threads=4, fps=24,
                         codec=v_sets['sets']['vcodec'],
                         preset=v_sets['sets']['compression'],
                         ffmpeg_params=["-crf", v_sets['sets']['vquality']])


if __name__ == '__main__':
    title_open = v_sets['sets']['dir_load'] + 'IMG_0039'
    title_save = v_sets['sets']['dir_save'] + 'IMG_0039'
    loadtitle = title_open + v_sets['sets']['load_ext']
    savetitle = title_save + v_sets['sets']['save_ext']

    cuts = [('00:00:00.00', '00:00:04.00'),
            ('00:00:14.00', '00:00:20.00')]

    edit_video(loadtitle, savetitle, cuts)
