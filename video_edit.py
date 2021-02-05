import os

import moviepy.editor as mvpy
import moviepy.video.fx.all as vfx
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.drawing import blit
from moviepy.video.tools.segmenting import findObjects
from moviepy.video.fx.mask_color import mask_color

import numpy as np

from effects import mask_img

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


class TrickyBugText(mvpy.TextClip):

    def blit_on(self, picture, t):
        """
        Returns the result of the blit of the clip's frame at time `t`
        on the given `picture`, the position of the clip being given
        by the clip's ``pos`` attribute. Meant for compositing.
        """
        return fix_problem_pos_mlt_clips(self, picture, t)


def edit_video(input_videos, savetitle, cuts):
    """
    Main function. Сценарий обработки видео.
    :param input_videos: указатели на видео, имя
        :type input_videos: list
    :param savetitle: имя для обработанного видео
        :type savetitle: str
    :return: None
    """
    clips = []
    tfreeze = mvpy.cvsecs(7.10)

    for movie, cut in zip(input_videos, cuts):
        clip = mvpy.VideoFileClip(movie, target_resolution=(1080, 1920)).subclip(*cut)
        clips.append(clip)

    im = mvpy.ImageClip('files/icon/window.png')
    regions = findObjects(im)

    comp_clips = [c.resize(r.size)
                      .set_mask(r.mask)
                      .set_pos(r.screenpos)
                  for c, r in zip([clips[2], clips[3]], [regions[1], regions[2]])]

    text_1 = edit_text("Moscow River", 'text_1')
    text_2 = edit_text("Moscow City", 'text_2')

    # logo_1 = add_img("files/icon/location.png", mark='text_1')
    # logo_2 = mvpy.ImageClip("files/icon/location.png", ismask=True)
    # logo_2 = add_img("files/icon/location.png", mark='text_2')

    represent_video = mvpy.concatenate_videoclips(clips)

    pre_final_clip = mvpy.CompositeVideoClip([represent_video,
                                              text_1,
                                              text_2,
                                              *comp_clips])

    # -------------------------------------------------------------------
    clip_before = pre_final_clip.subclip(pre_final_clip.start, tfreeze)
    clip_after = pre_final_clip.subclip(tfreeze, pre_final_clip.end)

    im_freeze = represent_video.to_ImageClip(tfreeze)
    painting = (represent_video.fx(vfx.painting, saturation=1.6, black=0.006)
                .to_ImageClip(tfreeze))

    painting_txt = (mvpy.CompositeVideoClip([painting,
                                             # logo_2.set_position(('center', 'center')),
                                             ])  # открытка
                    .add_mask()
                    .set_duration(3)
                    .crossfadein(0.5)
                    .crossfadeout(0.5))

    painting_fading = mvpy.CompositeVideoClip([im_freeze, painting_txt])

    final_clip = mvpy.concatenate_videoclips([clip_before,
                                              painting_fading.set_duration(3),
                                              clip_after])

    save_video(final_clip, savetitle)

    for v in clips:
        v.close()


def add_text_background(text):
    txt_col = text.on_color(size=(text.w + 10, text.h - 10),
                            color=(0, 0, 0), col_opacity=0.6)
    return txt_col.set_pos(text.pos)


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
    input_videos = []
    for video, ext, num in zip(['IMG_0039', 'IMG_0833', 'IMG_0040', 'IMG_0042'],
                               ['.MOV', '.MP4', '.mp4', '.mp4'],
                               [2, 1, 1, 1]):
        title_open = v_sets['sets']['dir_load'] + video
        loadtitle = [title_open + ext] * num
        input_videos += loadtitle

    title_save = v_sets['sets']['dir_save'] + 'IMG_0039'
    savetitle = title_save + v_sets['sets']['save_ext']

    cuts = [('00:00:00.00', '00:00:04.00'),
            ('00:00:14.00', '00:00:20.00'),
            ('00:00:12.00', '00:00:22.00'),
            ('00:00:03.00', '00:00:13.00'),
            ('00:00:02.00', '00:00:12.00')]

    edit_video(input_videos, savetitle, cuts)
