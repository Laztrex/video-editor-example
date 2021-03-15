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


class VideoEdit:

    def __init__(self, input_videos, savetitle, cuts):
        self.clips = []
        self.tfreezes = [mvpy.cvsecs(15.10), mvpy.cvsecs(23.10)]
        self.input_videos = input_videos
        self.cuts = cuts
        self.save_title = savetitle

    def run(self):
        for movie, cut in zip(self.input_videos, self.cuts):
            clip = mvpy.VideoFileClip(movie, audio=False,
                                      target_resolution=(1080, 1920)).subclip(*cut)  # resize_algorithm='bicublin'
            self.clips.append(clip)

        text = [self.get_text(text, mode) for text, mode in zip([t_sets['loc1'], t_sets['loc2']],
                                                                ['text_2', 'text_2'])]

        represent_video = mvpy.concatenate_videoclips(self.clips)

        clips_slices = self.slices_videos(
            mvpy.CompositeVideoClip([represent_video,
                                     *self.compilations(
                                         self.get_regions()
                                     )])
        )

        painting_fading = self.painting_gen(video=represent_video,
                                            text=text,
                                            sizes_screen=[text[0].size, text[1].size])

        final_clip = mvpy.concatenate_videoclips([next(clips_slices),
                                                  next(painting_fading),
                                                  next(clips_slices),
                                                  next(painting_fading),
                                                  next(clips_slices)]
                                                 )

        self.save_video(final_clip, self.save_title)

        for v in self.clips:
            v.close()

    def painting_gen(self, video, text, sizes_screen):
        for idx, tfreeze in enumerate(self.tfreezes):
            im_freeze = video.to_ImageClip(tfreeze)
            painting = (video.fx(vfx.blackwhite)  # RGB='CRT_phosphor'
                        .to_ImageClip(tfreeze))

            painting_txt = (mvpy.CompositeVideoClip([painting
                                                    .resize(lambda t: 1 + .01 * (3 - t)),
                                                     text[idx]
                                                    .resize(height=sizes_screen[idx][1] * 4)
                                                    .resize(lambda t: 1 + .01 * t)
                                                    .set_position(('center', 'center'))
                                                    .resize(sizes_screen[idx])
                                                     ])  # открытка
                            .add_mask()
                            )

            yield mvpy.CompositeVideoClip([im_freeze, painting_txt]) \
                .set_duration(3) \
                .crossfadeout(0.3)

    def compilations(self, regions):
        return [c.resize(r.size)
                    .set_mask(r.mask)
                    .set_pos(r.screenpos)
                    .set_duration(sec_dur)
                    .set_start(sec_st)
                for c, r, (sec_st, sec_dur) in zip(
                [self.clips[1], self.clips[2], self.clips[2], self.clips[3], self.clips[3]],
                [regions[1], regions[2], regions[1], regions[2], regions[2]],
                [(0, 10), (0, 10), (10, 7), (10, 7), (17, 7)]
            )]

    def slices_videos(self, work_vid):
        for x, y in zip([work_vid.start, self.tfreezes[0], self.tfreezes[1]],
                        [self.tfreezes[0], self.tfreezes[1], work_vid.end]):
            yield work_vid.subclip(x, y)

    def get_text(self, text, mode, track=False):
        text = mvpy.TextClip(text,
                             font=t_sets['sets'][mode]['font'],
                             fontsize=t_sets['sets'][mode]['fontsize'],
                             color=t_sets['sets'][mode]['color'],
                             stroke_color=t_sets['sets'][mode]['bg_clr'],
                             kerning=t_sets['sets'][mode]['kerning']
                             # bg_color=t_sets[mark]['bg_clr']
                             )
        if track:
            traj = Trajectory.load_list(t_sets['sets'][mode]['tracking'])
            for i in traj[:1]:
                text = text.set_position(i)

        return text

    def add_text_background(self, text):
        txt_col = text.on_color(size=(text.w + 10, text.h - 10),
                                color=(0, 0, 0), col_opacity=0.6)
        return txt_col.set_pos(text.pos)

    def get_regions(self):
        im = mvpy.ImageClip('files/icon/window.png')
        return findObjects(im)

    def save_video(self, clip, savetitle, path='media/save'):
        path = os.path.join(path)
        os.makedirs(path, exist_ok=True)

        clip.write_videofile(savetitle, threads=8, fps=24,
                             codec=v_sets['sets']['vcodec'],
                             preset=v_sets['sets']['compression'],
                             ffmpeg_params=["-crf", v_sets['sets']['vquality']],
                             remove_temp=True)


if __name__ == '__main__':
    inputs = []
    for movie, ext, num in zip(['IMG_0833', 'IMG_0041', 'IMG_0040', 'IMG_0042'],
                               ['.MP4', '.mp4', '.mp4', '.mp4'],
                               [1, 1, 1, 1]):
        title_open = v_sets['sets']['dir_load'] + movie
        loadtitle = [title_open + ext] * num
        inputs += loadtitle

    title_save = v_sets['sets']['dir_save'] + 'IMG_0039'
    title = title_save + v_sets['sets']['save_ext']

    timings = [('00:00:07.00', '00:00:17.00'),
               ('00:00:42.00', '00:00:49.00'),
               ('00:00:03.00', '00:00:10.00'),
               ('00:00:02.00', '00:00:12.00')]

    editor = VideoEdit(input_videos=inputs,
                       savetitle=title,
                       cuts=timings)
    editor.run()
# TODO: прямоугольник вокруг врезанных видео исчезающий
# TODO: звукорежиссёрить
# TODO: resize_algorithms