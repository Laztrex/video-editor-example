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
        'font': 'Courier',
        'fontsize': 120,
        'color': 'black',
        'bg_clr': 'gray35',
        'pos': ('center', 0.6),
        'start': (0, 1),
        'end': (0, 6.958),
        'fadein': 0.5,
        'fadeout': 0.5
    },

    'text_2': {
        'font': 'Courier',
        'fontsize': 120,
        'color': 'black',
        'bg_clr': 'gray35',
        'pos': ('left', 0.6),
        'start': (0, 6),
        'end': (0, 9.999),
        'fadein': 0.5,
        'fadeout': 0.5
    },
}

# from moviepy.video.tools.tracking import manual_tracking, Trajectory
# trajectories = manual_tracking(clip, t1=1, t2=7,
#                                nobjects=1, savefile="track.txt")
# trajectories = manual_tracking(clip, t1=7, t2=10,
#                                nobjects=1, savefile="track2.txt")
