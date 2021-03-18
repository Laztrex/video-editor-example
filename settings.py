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
            'fontsize': 30,
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
                'fontsize': 250,
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

# from moviepy.video.tools.tracking import manual_tracking
# import moviepy.editor as mvpy

# coor = {1: [], 2: [], 3: []}

# def get_line(x, y, k):
#     start = 2000
#     for i in range(x, x + 4000, 1):
#         start += 10
#         if start > 6500:
#             break
#         yield start, i, k * i + y
#
#
# total_1 = []
# total_2 = []
# total_3 = []
#
# with open("files/tracking/track.txt", 'r') as file:
#     with open("files/tracking/end_titre.txt", 'w') as file_write:
#         for idx, i in enumerate(file.readlines()[1:]):
#             print(i)
#             if idx < 2:
#                 coor[1].append(i.split())
#             elif 4 > idx >= 2:
#                 coor[2].append(i.split())
#             else:
#                 coor[3].append(i.split())
#
#             coors_1 = get_line(1188, 288, 0.0777)
#             coors_2 = get_line(725, 653, -0.486)
#             coors_3 = get_line(680, 520, -0.25)
#
#             total_1 = [i for i in coors_1]
#             total_2 = [i for i in coors_2]
#             total_3 = [i for i in coors_3]
#
#             file_write.writelines([str(i[0][0]) + '	' + str(i[0][1]) + '	' + str(i[0][2]) + '	'
#                                    + str(i[1][0]) + '	' + str(i[1][1]) + '	' + str(i[1][2]) +
#                                    '	' + str(i[2][0]) + '	' + str(i[2][1]) + '	' + str(i[2][2]) + '\n'
#                                    for i in zip(total_1, total_2, total_3)])

