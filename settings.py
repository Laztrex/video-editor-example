VIDEO_SCENARIOS = {
    'sets': {
        'vcodec': "libx264",
        'vquality': "5",
        'compression': "ultrafast",  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        'dir_load': "media/load/",
        'dir_save': "media/save/",
        'load_ext': ".mov",
        'save_ext': '.mp4',
    },
}

TEXT_SCENARIOS = {
    'loc1': "Moscow City",
    'loc2': "Vorobyovy\nHills",

    'sets':
        {'text_1': {
            'font': 'Amiri-regular',
            'fontsize': 20,
            'color': 'grey',
            'bg_clr': 'gray35',
            'pos': ('center', 0.6),
            # 'start': (0, 1),
            # 'end': (0, 6.958),
            'fadein': 0.3,
            'fadeout': 0.3,
            'kerning': 2,

            'tracking': 'files/tracking/end_titre.txt'
        },

            'text_2': {
                'font': 'AvantGarde-Bold',  # AvantGarde-Book
                'fontsize': 1000,
                'color': 'grey',
                'bg_clr': 'gray35',
                'pos': ('left', 0.6),
                'start': (0, 6),
                'end': (0, 9.999),
                'fadeout': 0.2,
                'kerning': 5,
            },

            'text_3': {
                'font': 'Amiri-regular',  # AvantGarde-Book
                'fontsize': 30,
                'color': 'grey',
                'bg_clr': 'gray35',
                'pos': ('left', 0.6),
                # 'start': (0, 6),
                # 'end': (0, 9.999),
                'fadein': 0.3,
                'fadeout': 0.3,
                'kerning': 2,

                'tracking': 'files/tracking/end_titre.txt'
            },

            'text_4': {
                'font': 'Amiri-regular',  # AvantGarde-Book
                'fontsize': 30,
                'color': 'grey',
                'bg_clr': 'gray35',
                'pos': ('left', 0.6),
                # 'start': (0, 6),
                # 'end': (0, 9.999),
                'fadein': 0.3,
                'fadeout': 0.3,
                'kerning': 2,

                'tracking': 'files/tracking/end_titre.txt'
            },
        }
}
