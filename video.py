import os


def clear(path):
    for i in os.listdir(path):
        os.remove(f'{path}/{i}')


def create_video_from_images(directory_to_frames):
    clear('output')
    os.system(f"ffmpeg -r 1 -i {directory_to_frames}/frame%01d.png -c:v libx265 -x265-params lossless=1 -tune grain output/output.mp4")


def extract_frames_from_video(directory_to_output_frames):
    os.system(f'ffmpeg -i output/output.webm -vf fps=1 -qscale 0  -crf 0 -b:v 40M {directory_to_output_frames}/frame%d.png')


if __name__ == '__main__':
    create_video_from_images('frames')
