import numpy as np
import shutil
import random

from decimal import getcontext, Decimal
from moviepy.editor import *
from PIL import Image, ImageSequence
from typing import Union, List


class GlitchEffect:
    def __init__(self, src, seed=0):
        self.pixel_tuple_len = None
        self.src = src
        self.img_mode = None

        self.input_arr = None
        self.output_arr = None

        self.curr_img_size = None

        self.glitch_max = 10.0
        self.glitch_min = 0.1

        self.dir_path = 'temp'

        self.seed = seed

    def start(self):
        original_prec = getcontext().prec
        getcontext().prec = 4

        if isinstance(self.src, (VideoFileClip, VideoClip)):
            result = self.__iterable_source(iterable_src=self.src.iter_frames(fps=24, dtype='uint8'), mode='video')
        elif isinstance(self.src, Image.Image):
            result = self.__iterable_source(iterable_src=ImageSequence.Iterator(Image.open(self.src)), mode='img')
        else:
            raise ValueError(f'Unknown type source file - {type(self.src)}')

        getcontext().prec = original_prec

        return result

    def __iterable_source(self, iterable_src, mode):
        if os.path.isdir(self.dir_path):
            shutil.rmtree(self.dir_path)
        os.mkdir(self.dir_path)

        step = 1
        glitch_amount, color_offset, scan_lines = 2., True, False

        glitched_images = []

        for idx, frame in enumerate(iterable_src):
            src_frame_path = os.path.join(self.dir_path, 'frame.png')
            Image.fromarray(frame).save(src_frame_path, compress_level=3)
            if not idx % step == 0:
                glitched_images.append([ImageClip(src_frame_path).set_duration(1 / 24),
                                        Image.open(src_frame_path).copy()][mode == 'img'])
                continue
            scan_lines, glitch_amount = (True, self.__change_glitch(glitch_amount, glitch_change=.4, cycle=False)) \
                if 35 > idx > 23 else (False, 2.)
            glitched_img = self.set_glitch_img(src_img=src_frame_path, glitch_amount=glitch_amount,
                                               color_offset=color_offset, scan_lines=scan_lines)
            file_path = os.path.join(self.dir_path, 'glitched_frame.png')
            glitched_img.save(file_path, compress_level=3)
            glitched_images.append([ImageClip(file_path).set_duration(1 / 24),
                                    Image.open(file_path).copy()][mode == 'img'])

        # Cleanup
        shutil.rmtree(self.dir_path)

        return glitched_images

    def set_glitch_img(self, src_img, glitch_amount, color_offset, scan_lines) -> Union[Image.Image, List[Image.Image]]:
        img = Image.open(src_img).convert('RGBA')
        # img = cv2.imread(src_img, cv2.IMREAD_UNCHANGED)

        self.pixel_tuple_len = len(img.getbands())
        self.curr_img_size = img.size
        self.img_mode = img.mode

        self.input_arr = np.asarray(img)
        self.output_arr = np.array(img)

        return self.__get_glitch_img(glitch_amount, color_offset, scan_lines)

    def __get_glitch_img(self, glitch_amount, color_offset, scan_lines):
        w, h = self.curr_img_size
        max_offset = int((glitch_amount ** 2 / 100) * w)
        doubled_glitch_amount = int(glitch_amount * 2)
        for shift_num in range(0, doubled_glitch_amount):

            if self.seed:
                self.__reset_rng_seed(offset=shift_num)

            current_offset = random.randint(-max_offset, max_offset)
            if current_offset == 0:
                continue
            if current_offset < 0:
                self.shift_left(-current_offset)
            else:
                self.shift_right(current_offset)

        if color_offset:
            # Get the next random channel we'll offset, needs to be before the random.randints
            # arguments because they will use up the original seed (if a custom seed is used)
            random_channel = self.__get_random_channel()
            # Add color channel offset if checked true
            self.conv_color(random.randint(-doubled_glitch_amount, doubled_glitch_amount),
                            random.randint(-doubled_glitch_amount,
                                           doubled_glitch_amount),
                            random_channel)

        if scan_lines:
            # Add scan lines if checked true
            self.set_lines()

        return Image.fromarray(self.output_arr, self.img_mode)

    def shift_left(self, offset):
        w, h = self.curr_img_size
        start_y = random.randint(0, h)
        chunk_height = random.randint(1, int(h / 4))
        chunk_height = min(chunk_height, h - start_y)
        stop_y = start_y + chunk_height

        # For copy
        start_x = offset
        # For paste
        stop_x = w - start_x

        left_chunk = self.input_arr[start_y:stop_y, start_x:]
        wrap_chunk = self.input_arr[start_y:stop_y, :start_x]
        self.output_arr[start_y:stop_y, :stop_x] = left_chunk
        self.output_arr[start_y:stop_y, stop_x:] = wrap_chunk

    def shift_right(self, offset):
        w, h = self.curr_img_size
        start_y = random.randint(0, h)
        chunk_height = random.randint(1, int(h / 4))
        chunk_height = min(chunk_height, h - start_y)
        stop_y = start_y + chunk_height

        stop_x = w - offset

        start_x = offset

        right_chunk = self.input_arr[start_y:stop_y, :stop_x]
        wrap_chunk = self.input_arr[start_y:stop_y, stop_x:]
        self.output_arr[start_y:stop_y, start_x:] = right_chunk
        self.output_arr[start_y:stop_y, :start_x] = wrap_chunk

    def conv_color(self, offset_x: int, offset_y: int, channel_index: int):
        w, h = self.curr_img_size
        offset_x = offset_x if offset_x >= 0 else w + offset_x
        offset_y = offset_y if offset_y >= 0 else h + offset_y

        self.output_arr[offset_y, offset_x:, channel_index] = self.input_arr[0, :w - offset_x, channel_index]
        self.output_arr[offset_y, :offset_x, channel_index] = self.input_arr[0, w - offset_x:, channel_index]
        self.output_arr[offset_y + 1:, :, channel_index] = self.input_arr[1:h - offset_y, :, channel_index]
        self.output_arr[:offset_y, :, channel_index] = self.input_arr[h - offset_y:, :, channel_index]

    def set_lines(self):
        self.output_arr[::2, :, :3] = [0, 0, 0]

    def __change_glitch(self, glitch_amount, glitch_change, cycle):
        glitch_amount = float(Decimal(glitch_amount) + Decimal(glitch_change))

        if glitch_amount < self.glitch_min:
            glitch_amount = float(
                Decimal(self.glitch_max) + Decimal(glitch_amount)) if cycle else self.glitch_min
        if glitch_amount > self.glitch_max:
            glitch_amount = float(Decimal(glitch_amount) % Decimal(
                self.glitch_max)) if cycle else self.glitch_max
        return glitch_amount

    def __get_random_channel(self) -> int:
        return random.randint(0, self.pixel_tuple_len - 1)

    def __reset_rng_seed(self, offset: int = 0):
        random.seed(self.seed + offset)

    @staticmethod
    def make_video(result_images):
        return concatenate_videoclips(result_images, method='compose').set_fps(24)

    @staticmethod
    def make_gif(result_images):
        result_images[0].save('glitched_my_func_4.gif',
                              format='GIF',
                              append_images=result[1:],
                              save_all=True,
                              duration=80,
                              loop=0)
