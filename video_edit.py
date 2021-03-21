import os

import moviepy.editor as mvpy
import moviepy.video.fx.all as vfx
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.segmenting import findObjects

from effects import masked_with_offsets

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets


class VideoEdit:

    def __init__(self, input_videos, savetitle, cuts):
        self.clips = []
        self.tfreezes = [mvpy.cvsecs(40.5), mvpy.cvsecs(83)]
        self.input_videos = input_videos
        self.cuts = cuts
        self.save_title = savetitle

    def painting_gen(self, video, text):
        """
        Генератор составных стилизованных стоп-кадров (+ здесь эффекта зума)
        :param video: видеофайл, откуда берутся стоп-кадры
            :type video: class VideoClip
        :param text: текст поверх кадра
            :type text: class TextClip
        :return:
        """
        for idx, tfreeze in enumerate(self.tfreezes):
            im_freeze = video.subclip(tfreeze)
            painting = (video.subclip(tfreeze).fx(vfx.blackwhite))  # RGB='CRT_phosphor'

            painting_txt = (mvpy.CompositeVideoClip([painting,
                                                     text[idx]
                                                    .resize(lambda t: (0.5 + 0.01 * t))
                                                    .resize(lambda t: (0.5 + 0.01 * t))
                                                    .set_pos('center')
                                                     ])
                            .add_mask()
                            )

            yield mvpy.CompositeVideoClip([im_freeze, painting_txt]) \
                .set_duration(2.5) \
                .crossfadeout(0.3)

    def slices_videos(self, work_vid):
        """
        Генератор подклипов для вставки динамических стоп-кадров (см. метод painting_gen)
        :param work_vid: исходный клип
            :type work_vid: class VideoClip
        """
        for x, y in zip([work_vid.start, self.tfreezes[0] + 2.5, self.tfreezes[1] + 2.5],
                        [self.tfreezes[0], self.tfreezes[1], work_vid.end]):
            yield work_vid.subclip(x, y)

