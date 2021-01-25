import os

import moviepy.editor as mvpy
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.drawing import blit

import numpy as np

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets


class TrickyBug(mvpy.TextClip):
    """
    Временное решение проблемы Multiple TextClips
    """

    def blit_on(self, picture, t):
        """
        Returns the result of the blit of the clip's frame at time `t`
        on the given `picture`, the position of the clip being given
        by the clip's ``pos`` attribute. Meant for compositing.
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
    video = mvpy.VideoFileClip(loadtitle)

    clips = []
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        clips.append(clip)

    final_clip = mvpy.concatenate_videoclips(clips)

    text_1 = edit_text("Москва-река", 'text_1')
    text_2 = edit_text("Москва-сити", 'text_2')

    final_clip = mvpy.CompositeVideoClip([final_clip, text_1, text_2])

    save_video(final_clip, savetitle)
    video.close()


def edit_text(text, mark):
    """
    Добавление титров
    :param text: текст
        :type text: str
    :param mark: указатель на настройки титров (для settings)
        :type mark: str
    :return: TextClip
    """
    text = TrickyBug(text,
                     font=t_sets[mark]['font'],
                     fontsize=t_sets[mark]['fontsize'],
                     color=t_sets[mark]['color'],
                     # bg_color=t_sets[mark]['bg_clr']
                     )

    traj = Trajectory.load_list(t_sets[mark]['tracking'])
    for i in traj:
        text = text.set_position(i)

    text = text.set_start(t_sets[mark]['start'])
    text = text.set_end(t_sets[mark]['end'])
    text = text.crossfadein(t_sets[mark]['fadein'])
    text = text.crossfadein(t_sets[mark]['fadeout'])

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
