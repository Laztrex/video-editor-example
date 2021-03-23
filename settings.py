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

    'img_list':
        ["media/load/1.jpg", "media/load/2.jpeg", "media/load/3.jpeg",
         "media/load/4.png", "media/load/5.jpeg", "media/load/6.jpeg"]

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
