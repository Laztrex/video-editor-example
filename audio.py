import moviepy.editor as mvpy


class AudioEditor:
    def __init__(self):
        self.main_track = None
        self.effects = []

    def add_main_track(self, track):
        self.main_track = mvpy.AudioFileClip(track).subclip(10, 154).audio_fadein(1).audio_fadeout(1)

    def add_effects(self, effects, times, vol=.3, vol_main=False):
        if vol_main and self.main_track:
            self.main_track = mvpy.concatenate_audioclips(
                [self.main_track.subclip(t_end=times[1]),
                 self.main_track.subclip(times[1], times[1] + times[0]).volumex(.8),
                 self.main_track.subclip(times[1] + times[0])]
            )
        self.effects.append(
            mvpy.AudioFileClip(effects).subclip(t_end=times[0]).set_start(times[1]).volumex(vol).audio_fadeout(.5)
        )

    def merge(self, effect=None):
        pass

    def extract_audio(self, video, cuts=(0, )):
        """
        Просто выделяем аудиодорожку видеофайла
        :return: None
        """
        audio = mvpy.AudioFileClip(video).subclip(*cuts).audio_fadeout(1)
        audio.write_audiofile("test.mp3")

    def get_track(self):
        return mvpy.CompositeAudioClip([self.main_track, *self.effects])
