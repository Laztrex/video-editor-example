import moviepy.editor as mvpy
import os

from settings import VIDEO_SCENARIOS as v_sets
from settings import TEXT_SCENARIOS as t_sets


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

    text_1 = edit_text("Это «Москва-река»", 'text_1')
    text_2 = edit_text("Это «Москва-сити»", 'text_2')

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
    text = mvpy.TextClip(text,
                         font=t_sets[mark]['font'],
                         fontsize=t_sets[mark]['fontsize'],
                         color=t_sets[mark]['color'],
                         # bg_color=t_sets[mark]['bg_clr']
                         )

    text = text.set_position(t_sets[mark]['pos'])
    text = text.set_start(t_sets[mark]['start'])
    text = text.set_end(t_sets[mark]['end'])
    text = text.set_duration(4)
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
