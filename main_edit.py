import os

import moviepy.editor as mvpy
import moviepy.video.fx.all as vfx
from moviepy.video.tools.tracking import Trajectory
from moviepy.video.tools.segmenting import findObjects

from effects import masked_with_offsets

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets


class VideoEdit:
    """
    v. Python 3.7.5

    Класс редактирования видео (демонстрация)
    """

    def __init__(self, input_videos, savetitle, cuts):
        self.clips = []
        self.tfreezes = [mvpy.cvsecs(12.10), mvpy.cvsecs(19.10)]
        self.input_videos = input_videos
        self.cuts = cuts
        self.save_title = savetitle

    def run(self):
        """
        Запуск редактора (демонстрационный режим)
        """
        for idx, (movie, cut) in enumerate(zip(self.input_videos, self.cuts)):
            clip = mvpy.VideoFileClip(movie, audio=False,
                                      target_resolution=(1080, 1920)).subclip(*cut)  # resize_algorithm='bicublin'

            if idx == 3:
                texts = self.get_text(["Text 1", "Text 2", "Text 3"], "text_1", track=True)
                clip_with_text = mvpy.CompositeVideoClip([clip, texts[0], texts[1], texts[2]]) \
                    .set_duration(clip.duration) \
                    .set_start(clip.start)
                self.clips += [clip, clip_with_text]
                continue

            self.clips.append(clip)

        text = self.get_text([t_sets['loc1'], t_sets['loc2']], 'text_2')
        represent_video = mvpy.concatenate_videoclips(self.clips[:-2])

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
                                                  next(clips_slices),
                                                  self.clips[-1]]
                                                 )

        self.save_video(final_clip, self.save_title)

        for v in self.clips:
            v.close()

    def painting_gen(self, video, text, sizes_screen):
        """
        Генератор составных стилизованных стоп-кадров (+ здесь эффекта зума)
        :param video: видеофайл, откуда берутся стоп-кадры
            :type video: class VideoClip
        :param text: текст поверх кадра
            :type text: class TextClip
        :param sizes_screen: размеры исходного текстового клипа (TextClip от метода get_text)
            :type sizes_screen: list
        :return:
        """
        for idx, tfreeze in enumerate(self.tfreezes):
            im_freeze = video.subclip(tfreeze)
            painting = (video.subclip(tfreeze).fx(vfx.blackwhite))  # RGB='CRT_phosphor'

            painting_txt = (mvpy.CompositeVideoClip([painting,
                                                     # .resize(height=sizes_screen[idx][1] * 4),
                                                     # .resize(lambda t: 1 + .01 * (3 - t)),
                                                     text[idx]
                                                    .resize(lambda t: (0.1 * t))
                                                    .resize(lambda t: (1 + 0.05 * t))
                                                     .set_pos('center')
                                                     # .resize(sizes_screen[idx])
                                                     ])  # открытка
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

    def compilations(self, regions):
        """
        Метод для генерирования набора видео для врезки в форму (см. метод get_regions)
        :param regions: координаты секторов для встраивания видео в форму
            :type regions: list(ImageClip, ...)
        :return: список разделённых по секторам клипов
        """

        mini_clip_1_ofs = masked_with_offsets(self.clips[1].resize(regions[2].size).set_duration(10), with_no_ofs=False)
        mini_clip_2_ofs = masked_with_offsets(self.clips[2].resize(regions[2].size), with_no_ofs=False)
        mini_clip_3_ofs = masked_with_offsets(self.clips[3].resize(regions[2].size), with_no_ofs=False)

        mini_clip_2 = masked_with_offsets(self.clips[2].resize(regions[2].size).set_duration(10))
        mini_clip_3 = masked_with_offsets(self.clips[3].resize(regions[2].size))

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
                [(0, 10), (0, 10),
                 (10, 7), (10, 7),
                 (17, 7)]
            )]

    def get_text(self, texts, mode, track=False):
        """
        Метод создаёт текстовый клип
        :param texts: Список строк текста для записи
            :type texts: list
        :param mode: Признак сетки параметров для текстового клипа (из settings.TEXT_SCENARIOS)
            :type mode: str
        :param track: Флаг для создания динамического текста. Параметры движения задаются в текстовом файле
        (см. settings.TEXT_SCENARIOS)
            :type track: bool
        :return: Текстовый клип
            :rtype class TextClip
        """
        gettings_trajectory = None
        total_texts = []
        for num_text, label in enumerate(texts):
            text = mvpy.TextClip(label,
                                 font=t_sets['sets'][mode]['font'],
                                 fontsize=t_sets['sets'][mode]['fontsize'],
                                 color=t_sets['sets'][mode]['color'],
                                 stroke_color=t_sets['sets'][mode]['bg_clr'],
                                 kerning=t_sets['sets'][mode]['kerning']
                                 )

            if track:

                if gettings_trajectory is None:
                    traj = Trajectory.load_list(t_sets['sets'][mode]['tracking'])
                    gettings_trajectory = traj[:len(texts)]

                text = text.set_position(gettings_trajectory[num_text])

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

    def get_regions(self):
        """
        Сегментирование на основе заданного паттерна (позднее настройки будут вынесены в settings)
        :return: список ImageClips с детектированными объектами на основе паттерна
            :rtype list(ImageClip, ...)
        """
        im = mvpy.ImageClip('files/icon/window.png')
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
# TODO: звукорежиссёрить
# TODO: resize_algorithms
