VIDEO_SCENARIOS = {
    'sets': {
        'vcodec': "libx264",
        'vquality': "24",
        'compression': "slow",  # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        'dir_load': "media/load/",
        'dir_save': "media/save/",
        'load_ext': ".mov",
        'save_ext': '.mp4',
    },
}

TEXT_SCENARIOS = {
    'text_1': {
        'font': 'Amiri-regular',
        'fontsize': 30,
        'color': 'grey',
        'bg_clr': 'gray35',
        'pos': ('center', 0.6),
        'start': (0, 1),
        'end': (0, 6.958),
        'fadein': 0.3,
        'fadeout': 0.3,

        'tracking': 'files/tracking/river.txt'
    },

    'text_2': {
        'font': 'Amiri-regular',
        'fontsize': 30,
        'color': 'grey',
        'bg_clr': 'gray35',
        'pos': ('left', 0.6),
        'start': (0, 6),
        'end': (0, 9.999),
        'fadein': 0.3,

        'tracking': 'files/tracking/towers.txt'
    },
}

# from moviepy.video.tools.tracking import manual_tracking, Trajectory
# trajectories = manual_tracking(clip, t1=1, t2=7,
#                                nobjects=1, savefile="track.txt")
# trajectories = manual_tracking(clip, t1=7, t2=10,
#                                nobjects=1, savefile="track2.txt")

# with open("files/tracking/towers.txt", 'r') as file:
#     with open("files/tracking/towers_3.txt", 'w') as wr:
#         for i in file.readlines()[1:]:
#             l = [int(a) for a in i.split()]
#             for m in l:
#                 u.append(m)
#                 u.append('	')
#             u.append(l[0])
#             u.append('	')
#             u.append(l[1] - 50)
#             u.append('	')
#             u.append(l[2])
#             wr.writelines([str(m) for m in u])
#             wr.write('\n')
#             u.clear()


# a1 = []
# a2 = []
# temp_a = []
# temp_a2 = []
# temp_b = []
# temp_e = []
# temp_c = []
# temp_f = []
#
# finish = []
# import numpy as np
#
# with open("files/tracking/river.txt", 'r') as file:
#     for i in file.readlines()[1:]:
#         a, b, c, d, e, f = i.split()
#         a1.append(a)
#         a2.append(d)
#         if int(a) < 2999:
#             for dx, i in enumerate([a, b, c, d, e, f]):
#                 finish.append(i)
#                 if dx != 5:
#                     finish.append('	')
#             finish.append('\n')
#         else:
#             temp_a.append(a)
#             temp_a2.append(d)
#             temp_b.append(int(b))
#             temp_e.append(int(e))
#             temp_c.append(int(c) + 400)
#             temp_f.append(int(f))
#
#     b1 = np.linspace(start=max(temp_b), stop=min(temp_b), num=len(temp_b), dtype=int)
#     c1 = np.linspace(start=min(temp_c), stop=max(temp_c), num=len(temp_c), dtype=int)
#
#     for j in range(len(b1)):
#         finish.append(temp_a[j])
#         finish.append('	')
#         finish.append(b1[j])
#         finish.append('	')
#         finish.append(c1[j])
#         finish.append('	')
#         finish.append(temp_a2[j])
#         finish.append('	')
#         finish.append(b1[j] - 150)
#         finish.append('	')
#         finish.append(c1[j])
#         finish.append('\n')
