import cv2
import numpy as np

import moviepy.editor as mvpy
from moviepy.video.tools.drawing import color_gradient
from moviepy.video.tools.tracking import manual_tracking
import moviepy.video.fx.all as vfx

from gif_glitch import GlitchEffect


def mask_img(img1, flag=True):
    """
    слияние картинки и иконок
    :param img1: картинка
    :param icon: имя иконки
    :param mode: weather/part_day/degree - меняентся пространство наслоения
    :param part_day: подсмотр координат в зависимости от части суток
    :return: изображение с иконками
    """
    img2 = cv2.imread(img1)
    # brows, bcols = img1.shape[:2]
    # rows, cols, channels = img2.shape
    #
    # roi = img1[0:rows, bcols - rows:bcols]
    #
    # img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    # mask_inv = cv2.bitwise_not(mask)
    #
    # img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
    # img2_fg = cv2.bitwise_and(img2, img2, mask=mask_inv)
    #
    # dst = cv2.add(img1_bg, img2_fg)
    # img2 = dst
    #
    #
    # img1[0:rows, bcols - rows:bcols] = img2

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    x, y, w, h = cv2.boundingRect(cnt)
    dst = img2[y:y + h, x:x + w]
    cv2.imwrite("001.png", dst)

    # return img1


def masked_with_offsets(video, speed_ofs=1, with_no_ofs=True):
    """
    Функция для доп. эффектов маски
    :param video: клип для трансформации
        :type video: class VideoClip
    :param speed_ofs: Скорость маски сдвига
        :type speed_ofs: float
    :param with_no_ofs: Флаг сдвига маски (True - вернуть и без сдига)
        :type with_no_ofs: bool
    :return: список клипов с преобразованной маской
        :rtype list с VideoClip
    """

    gradient = color_gradient(video.size,
                              p1=(0, 250), p2=(250, 125),
                              col1=[225, 129, 255], col2=[225, 129, 255],
                              shape='linear')
    gradient_mask = mvpy.ImageClip(gradient, transparent=True) \
        .set_duration(video.duration) \
        .set_pos(("center", "center")) \
        .set_opacity(.25)

    painting_video = (mvpy.CompositeVideoClip(
        [video, gradient_mask
            .set_position(lambda t: ([(0 + speed_ofs * 25 * t), 'center'][with_no_ofs], 'center')),
         ])
    )

    return painting_video


def set_tracking():
    def get_line(x, y, k, step):
        start = 0
        x = (x[0] * 2, x[1] * 2)
        y = y * 2

        cs = np.linspace(x[0], x[1], step)
        for i in cs:
            start += 1
            if start < 9001:
                yield start, i, k * i + y
            else:
                break

    with open("files/tracking/end_titre.txt", 'w') as file_write:
        coors_1 = get_line((1130, 1450), 1143, -0.75, 15000)
        coors_2 = get_line((640, 740), 1010, -0.75, 17000)
        coors_3 = get_line((710, 575), 907, -0.75, 17000)

        total_1 = [i for i in coors_1]
        total_2 = [i for i in coors_2]
        total_3 = [i for i in coors_3]

        file_write.writelines([str(i[0][0]) + '	' + str(i[0][1]) + '	' + str(i[0][2]) + '	'
                               + str(i[1][0]) + '	' + str(i[1][1]) + '	' + str(i[1][2]) +
                               '	' + str(i[2][0]) + '	' + str(i[2][1]) + '	' + str(i[2][2]) + '\n'
                               for i in zip(total_1, total_2, total_3)])


def glitch_effect(video, mode='video', fps=None, opt=0, loop=0,
               colors=None, verbose=True):
    # temp_dir = os.path.join('temp', 'pre_gif.gif')
    glitcher = GlitchEffect(src=video.subclip(t_start=3, t_end=5))
    result = glitcher.start()

    res_glitch_video = mvpy.concatenate_videoclips([video.subclip(t_end=3),
                                                    getattr(glitcher, f'make_{mode}')(result),
                                                    video.subclip(t_start=5)])
    return res_glitch_video


def matrix_effect():
    pass
