import numpy as np
import imageio


class GlitchEffect:
    def __init__(self, src_gif):
        open_gif = imageio.imread(src_gif)
        self.input_arr = np.asarray(open_gif)
        self.output_arr = np.array(open_gif)

    def start(self):
        pass

    def set_glitch_img(self):
        pass

    def shift_lef(self):
        pass

    def shift_right(self):
        pass

    def conv_color(self):
        pass

    def set_lines(self):
        pass

    def randomizer(self):
        pass
