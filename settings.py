VIDEO_SCENARIOS = {
    'sets': {
        'vcodec': "libx264",
        'vquality': "1",
        'compression': "ultrafast",  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        'dir_load': "media/load/",
        'dir_save': "media/save/",
        'load_ext': ".mov",
        'save_ext': '.mp4',
    },

    'movie_list': ['start.mp4', '7.mp4', 'IMG_0043.mp4', 'IMG_0037.mp4', 'IMG_0039.mp4', 'IMG_0045.mp4', 'IMG_0833.MP4',
                   'IMG_0044.mp4', 'IMG_0041.mp4', 'IMG_0050.mp4', 'IMG_0040.mp4', 'IMG_0042.mp4'],

    'img_list':
        ["media/load/1.jpg", "media/load/2.jpeg", "media/load/3.jpeg",
         "media/load/4.png", "media/load/5.jpeg", "media/load/6.jpeg"],

    'effects_img_list': ["media/load/videoplayback_3.mp4", "media/load/videoplayback_4.mp4",
                         "media/load/videoplayback_5.mp4", "media/load/videoplayback.mp4",
                         "media/load/videoplayback_6.mp4", "media/load/videoplayback_7.mp4"]

}


AUDIO_SCENARIOS = {
    'track': "media/load/sample_2.wav",
    'load_effect': "media/load/load_sound.mp3"
}


TEXT_SCENARIOS = {
    'loc1': "Moscow City",
    'loc2': "Vorobyovy\nHills",

    'sets':
        {'titre': {
            'font': 'Amiri-regular',
            'fontsize': 20,
            'color': 'grey',
            'stroke_color': 'grey',
            'kerning': 1,

        },

            'zoom_city': {
                'font': 'AvantGarde-Bold',  # AvantGarde-Book
                'fontsize': 1000,
                'color': 'grey',
                'stroke_color': 'gray35',
                'kerning': 5,
            },

            'loading': {
                'font': 'Amiri-regular',
                'fontsize': 30,
                'color': 'white',
            },

            'tracking': 'files/tracking/end_titre.txt'
        }
}
