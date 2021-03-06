import os

import moviepy.editor as mvpy
import moviepy.video.fx.all as vfx
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.segmenting import findObjects

from effects import masked_with_offsets

from audio import AudioEditor

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets
from settings import AUDIO_SCENARIOS as a_sets


class VideoEdit:
    """
    Python 3.7.5

    Класс редактирования видео (демонстрация)
    """

    def __init__(self, input_videos, savetitle, cuts):
        self.clips = []
        self.tfreezes = [mvpy.cvsecs(40), mvpy.cvsecs(85)]
        self.input_videos = input_videos
        self.cuts = cuts
        self.save_title = savetitle
        self.audio = AudioEditor()

    def spec_image_video_sequence(self, materials, mask, cuts=None, img=False, *args, **kwargs):
        for media in materials:
            yield mvpy.ImageClip(media, *args, **kwargs) \
                .resize(mask.size) \
                .set_mask(mask.mask) \
                .set_pos(mask.screenpos) \
                .crossfadein(1) \
                .crossfadeout(1) if img else \
                mvpy.VideoFileClip(media, audio=False,
                                   target_resolution=mask.size).subclip(*cuts) \
                    .set_mask(mask.mask) \
                    .set_pos(mask.screenpos) \
                    .set_duration(5) \
                    .crossfadein(1) \
                    .crossfadeout(1)

    def masked_effects_for_img(self, videos, size_list, cuts_list=None):
        for idx, (vid_name, size, cut) in enumerate(zip(videos, size_list, cuts_list)):
            vid = mvpy.VideoFileClip(vid_name, audio=False,
                                     target_resolution=size).subclip(*cut)
            masked_clip = vid.fx(vfx.mask_color, color=[0, 0, 0], thr=110, s=5)

            opacity, fdin, fdout = v_sets['effects'].get(vid_name, (.3, 1., .3))
            masked_clip = masked_clip.set_start([[5 * idx - 3, 0][idx == 0], 2][idx == 1]) \
                .set_opacity(opacity).crossfadein(fdin).crossfadeout(fdout)

            yield masked_clip.set_pos(('center', 'center')) if not idx == 5 else masked_clip.set_pos(('center', 460))

    def run(self):
        """
        Запуск редактора (демонстрационный режим)
        """

        mask_im = self.get_regions('files/icon/window_img.png')[2]

        images_seq = self.spec_image_video_sequence(v_sets['img_list'],
                                                    mask=mask_im, img=True, duration=5)

        first = mvpy.VideoFileClip(self.input_videos[0],
                                   audio=False, target_resolution=(1080, 1920)).subclip(*self.cuts[0])

        effects_img = list(self.masked_effects_for_img(['media/load/Loading Effect.mp4'] + v_sets['effects_img_list'],
                                                       size_list=[(332, 572), (680, 1100), (480, 840),
                                                                  (580, 940), (720, 1100),
                                                                  (100, 300), (670, 1100)],
                                                       cuts_list=[('00:00:02.00', '00:00:04.00'),
                                                                  ('00:00:00.00', '00:00:04.30'),
                                                                  ('00:00:14.00', '00:00:18.30'),
                                                                  ('00:00:17.00', '00:00:21.30'),
                                                                  ('00:00:07.00', '00:00:11.30'),
                                                                  ('00:00:20.00', '00:00:24.30'),
                                                                  ('00:00:32.00', '00:00:36.30')
                                                                  ]))

        self.clips.append(self.compositing_videos(
            [first,
             mvpy.concatenate_videoclips(list(images_seq))
                 .set_start(2)
                 .resize(.75)
                 .set_pos(('center', 'center')),
             *effects_img]
        ).fadeout(1))

        self.load_videos()

        represent_video = mvpy.concatenate_videoclips(self.clips[1:-2])
        precompiling_clips = self.compilations(self.clips[5:-1], self.get_regions())

        text_clip_1, text_clip_2 = self.get_text(["Loading...", "Loading..."], **t_sets['sets']['loading'])

        loading_effect = self.loading_imit(precompiling_clips[0], precompiling_clips[1])

        compiling_clips = [text_clip_1
                               .set_duration(3)
                               .set_position((1705, 75))
                               .set_start(33),
                           text_clip_2
                               .set_duration(3)
                               .set_position((1705, 225))
                               .set_start(33),
                           *loading_effect,
                           *precompiling_clips[2:]]

        clips_slices = self.slices_videos(
            self.compositing_videos([represent_video, *compiling_clips])
        )

        painting_fading = self.painting_gen(video=represent_video,
                                            text=self.get_text([t_sets['loc1'], t_sets['loc2']],
                                                               **t_sets['sets']['zoom_city']
                                                               ))

        final_clip = mvpy.concatenate_videoclips([
            self.clips[0],
            next(clips_slices),
            next(painting_fading),
            next(clips_slices),
            next(painting_fading),
            next(clips_slices),
            self.clips[-1]]
        )

        self.audio.add_main_track(a_sets['track'])
        self.audio.add_effects(a_sets['load_effect'], (4, 69))
        self.audio.add_effects(a_sets['label_effect'], (2.5, 36 + self.tfreezes[0]), vol=.9, vol_main=True)
        self.audio.add_effects(a_sets['label_effect'], (2.5, 36 + self.tfreezes[1]), vol=.9, vol_main=True)

        self.save_video(final_clip.set_audio(self.audio.get_track()), self.save_title)

        for v in self.clips:
            v.close()

    def load_videos(self):
        for idx, (movie, cut) in enumerate(zip(self.input_videos[1:], self.cuts[1:])):
            clip = mvpy.VideoFileClip(movie, audio=False,
                                      target_resolution=(1080, 1920)).subclip(*cut)  # resize_algorithm='bicublin'
            if idx == 0:
                clip = clip.fadein(1).fadeout(2)
            if idx == 9:
                texts = self.get_text(["good day", "loc: Moscow", "made in MoviePy"],
                                      track=True, **t_sets['sets']['titre'],
                                      )
                clip_with_text = self.compositing_videos([clip
                                                          # .resize((clip.size[0] * 2, clip.size[1] * 2))
                                                             ,
                                                          texts[0]
                                                          # .resize((texts[0].size[0] * 2, texts[0].size[1] * 2))
                                                             ,
                                                          texts[1]
                                                          # .resize((texts[1].size[0] * 2, texts[1].size[1] * 2))
                                                             ,
                                                          texts[2]
                                                          # .resize(
                                                          #      (texts[2].size[0] * 2, texts[2].size[1] * 2))
                                                          ]) \
                    .resize(clip.size) \
                    .set_start(clip.start) \
                    .fadeout(1)
                self.clips += [clip, clip_with_text]
                continue

            self.clips.append(clip)

    def loading_imit(self, video1, video2):
        before1, before2 = video1.subclip(0, 2).fx(vfx.blink, .3, .3), video2.subclip(0, 2).fx(vfx.blink, .3, .3)
        after1, after2 = video1.subclip(2).set_start(35), video2.subclip(2).set_start(35)
        return [before1, before2, after1, after2]

    def compositing_videos(self, list_materials):
        return mvpy.CompositeVideoClip(list_materials)

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

            painting_txt = self.compositing_videos([painting,
                                                    text[idx]
                                                   .resize(lambda t: (0.5 + 0.01 * t))
                                                   .resize(lambda t: (0.5 + 0.01 * t))
                                                   .set_pos('center')
                                                    ]).add_mask()

            yield self.compositing_videos([im_freeze, painting_txt]) \
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

    def compilations(self, videos, regions):
        """
        Метод для генерирования набора видео для врезки в форму (см. метод get_regions)
        :param regions: координаты секторов для встраивания видео в форму
            :type regions: list(ImageClip, ...)
        :return: список разделённых по секторам клипов
        """

        mini_clip_1_ofs = masked_with_offsets(videos[0].resize(regions[2].size).set_duration(13), speed_ofs=.77,
                                              with_no_ofs=False)
        mini_clip_2_ofs = masked_with_offsets(videos[1].resize(regions[2].size).set_duration(11.30), speed_ofs=.88,
                                              with_no_ofs=False)
        mini_clip_3_ofs = masked_with_offsets(videos[2].resize(regions[2].size).set_duration(10), with_no_ofs=False)

        mini_clip_2 = masked_with_offsets(videos[1].resize(regions[2].size).set_duration(13))
        mini_clip_3 = masked_with_offsets(videos[2].resize(regions[2].size).set_duration(11.30))

        return [c.resize(r.size)
                    .set_mask(r.mask)
                    .set_pos(r.screenpos)
                    .set_duration(c_dur)
                    .set_start(c_st)

                for c, r, (c_st, c_dur) in zip(
                [mini_clip_1_ofs, mini_clip_2,
                 mini_clip_3, mini_clip_2_ofs,
                 mini_clip_3_ofs],
                [regions[2], regions[1],
                 regions[2], regions[1],
                 regions[2]],
                [(33, 13), (33, 13),
                 (46, 11.30), (46, 11.30),
                 (57.30, 10)]
            )]

    def get_text(self, texts, track=False, *args, **kwargs):
        """
        Метод создаёт текстовый клип
        :param texts: Список строк текста для записи
            :type texts: list
        :param track: Флаг для создания динамического текста. Параметры движения задаются в текстовом файле
        (см. settings.TEXT_SCENARIOS)
            :type track: bool
        :return: Текстовый клип
            :rtype class TextClip
        """
        gettings_trajectory = None
        total_texts = []
        for num_text, label in enumerate(texts):
            text = mvpy.TextClip(label, **kwargs)

            if track:

                if gettings_trajectory is None:
                    traj = Trajectory.load_list(t_sets['sets']['tracking'])
                    gettings_trajectory = traj[:len(texts)]

                text = text.set_position(gettings_trajectory[num_text])

                text = text.set_duration(8)
                # text = text.crossfadein(1)
                text = text.crossfadeout(1)
            total_texts.append(text)
        return total_texts

    def add_text_background(self, text):
        """
        Добавление текста на цветном фоне
        :param text: класс текстового клипа для записи
            :type text: class TextClip
        :return: модифицированный TextClip
        """
        txt_col = text.on_color(size=(text.w + 10, text.h - 10),
                                color=(0, 0, 0), col_opacity=0.6)
        return txt_col.set_pos(text.pos)

    def get_regions(self, path='files/icon/window.png'):
        """
        Сегментирование на основе заданного паттерна (позднее настройки будут вынесены в settings)
        :return: список ImageClips с детектированными объектами на основе паттерна
            :rtype list(ImageClip, ...)
        """
        im = mvpy.ImageClip(path)
        return findObjects(im)

    def save_video(self, clip, savetitle, path='media/save'):
        """
        Метод сохранение отредактированного видео
        :param clip: финальное видео
            :type clip: VideoClip
        :param savetitle: имя сохранённого файла
            :type savetitle: str
        :param path: путь к видеофайлу
            :type path: str
        """
        path = os.path.join(path)
        os.makedirs(path, exist_ok=True)

        clip.write_videofile(savetitle, threads=8, fps=24, audio_bitrate="1000k",
                             codec=v_sets['sets']['vcodec'],
                             preset=v_sets['sets']['compression'],
                             ffmpeg_params=["-c:a", "copy", "-c:v", "libx264", "-crf", "0"],
                             remove_temp=True, audio_codec="aac")


if __name__ == '__main__':
    inputs = []
    for movie in v_sets['movie_list']:
        title_open = [v_sets['sets']['dir_load'] + movie]
        inputs += title_open

    title_save = v_sets['sets']['dir_save'] + 'IMG_0039'
    title = title_save + v_sets['sets']['save_ext']

    timings = [('00:00:11.00', '00:00:47.00'),
               ('00:00:00.00', '00:00:08.45'),
               ('00:00:00.00', '00:00:10.00'),
               ('00:00:00.00', '00:00:10.00'),
               ('00:00:00.45', '00:00:18.00'),
               ('00:00:07.00', '00:00:18.30'),
               ('00:00:01.00', '00:00:11.00'),
               ('00:00:40.00', '00:00:49.00'),
               ('00:00:00.00', '00:00:07.00'),
               ('00:00:01.00', '00:00:12.00'),
               ('00:00:02.00', '00:00:16.00')]

    editor = VideoEdit(input_videos=inputs,
                       savetitle=title,
                       cuts=timings)
    editor.run()
# TODO: звукорежиссёрить
# TODO: resize_algorithms
