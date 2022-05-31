import datetime

import bitstring
import os
from PIL import Image
from database import MongoDb
from video import create_video_from_images, extract_frames_from_video
from natsort import natsorted, ns
from collections import Counter
import youtube as yt


def multiply_every_binary_by_three_and_change_to_rgb(binary):
    """
    multiply every binary number by three so it can be
    converted into photo(rgb
    :param binary:
    :return:
    """

    return [(0, 0, 0) if number == '0' else (1, 1, 1) for number in binary]


def convert_to_binary(bytes_to_convert):
    """
    if it is first call add delimiter, the convert to binary
    :param bytes_to_convert:
    :return:
    """
    return bitstring.BitArray(bytes_to_convert).bin


def rgb_to_binary_string(rgb):
    return [''.join(['1' if y == 255 else '0' for y in x]) for x in rgb]


def group_rgb(bits):
    return [bits[d: d + 8] for d, x in enumerate(bits) if not d % 8]


def convert_rgb_with_security_num_to_normal(security_num, bits):
    return [int(Counter(bits[d: d + security_num]).most_common(1)[0][0]) for d, x in enumerate(bits) if not d % security_num]


def binary_list_to_byte(binary_string):
    output_bytes = b''
    for i in binary_string:
        output_bytes += bitstring.BitArray(f'0b{i}').tobytes()
    return output_bytes


def frame_to_bytes(path_to_file):
    rgb = list(Image.open(path_to_file).getdata())
    sorted_rgb = group_rgb(rgb)
    x = binary_list_to_byte(rgb_to_binary_string(sorted_rgb))
    print(x)
    # print(x)


class CreateImages:
    def __init__(self, filename, username, security_num):
        self.clear()
        self.filename = filename
        self.security_num = security_num
        self.number_of_bytes_read_at_one_time = int(
            259200 / self.security_num)  # 1920 * 1080 / 8 / divided by sec number. It must be converted to int,
        # so it can cause trouble
        self.basic_file_name_for_created_photos = 'frame'
        self.basic_dir_for_created_photos = 'frames'
        self.size_of_file = 0
        self.name_of_file = filename.split('/')[-1]
        self.username = username

        self.mongodb = MongoDb(username)

    def read_file(self, filename):
        """
        read data, only X bytes to not exceed memory. if no more bytes
        then while loop stops, always(hope so) with no bytes b''
        :param filename:
        :return:
        """
        num = 1
        with open(filename, 'rb') as file:
            data = file.read(self.number_of_bytes_read_at_one_time)
            self.deal_with_input_bytes(data, num)
            num += 1
            while data:
                data = file.read(self.number_of_bytes_read_at_one_time)
                self.deal_with_input_bytes(data, num)
                num += 1

    def deal_with_input_bytes(self, bytes_input, number):
        self.size_of_file += len(bytes_input)
        binary = []
        for i in convert_to_binary(bytes_input):
            if i == '0':
                binary.extend([0] * self.security_num)
            else:
                binary.extend([1] * self.security_num)
        # multiplied_binary_by_3_changed_to_rgb = multiply_every_binary_by_three_and_change_to_rgb(binary)
        # print(multiplied_binary_by_3_changed_to_rgb)
        self.create_image_from_bits(binary, number)

    def security_checks(self):
        """
        after youtube's policy change, security checks no longer apply

        """
        return True

    def create_image_from_bits(self, bits, number):
        """TODO if delimiter exceed create another photo"""
        image = Image.new('1', (1920, 1080))
        image.putdata(bits)
        image.save(f'{self.basic_dir_for_created_photos}/'
                   f'{self.basic_file_name_for_created_photos}{number}.png')

    def read_binary_from_image(self, number):
        return list(Image.open(f'{self.basic_dir_for_created_photos}/'
                               f'{self.basic_file_name_for_created_photos}{number}.png').getdata())

    def clear(self):
        for i in os.listdir('frames'):
            os.remove(f'frames/{i}')

    def main(self):
        self.read_file(self.filename)
        self.mongodb.insert_new_video_metadata(self.name_of_file, self.size_of_file)
        create_video_from_images('frames')
        """
        Due to change of Youtube's policy about API, you have to apply for the API 
        access. Instead use manual uploading. Download function should still work
        """
        if result := self.security_checks:
            yt.upload(datetime.datetime.now(), self.name_of_file, 'output\\output.mp4')
        else:
            return f"Security Check didn't pass due to {result}"


class CreateFileFromVideo:
    def __init__(self, filename, username, security_number, local=False):
        self.clear()
        extract_frames_from_video('output_frames')
        mongodb = MongoDb(username)
        self.size_of_file = mongodb.get_size_of_the_file(filename)['length_of_the_file']
        self.current_size = 0
        self.filename = filename
        self.local = local
        self.security_num = security_number

    def clear(self):
        for i in os.listdir('output_frames'):
            os.remove(f'output_frames/{i}')

    def extract_bytes_from_photos(self, filename_of_frame):
        rgb = list(Image.open(f'output_frames/{filename_of_frame}').getdata())
        if not self.local:
            rgb = ['255' if max(x) in range(128, 256) else '0' for x in rgb]
        rgb_after_checking_security_number = convert_rgb_with_security_num_to_normal(self.security_num, rgb)
        sorted_rgb = group_rgb(rgb_after_checking_security_number)
        bytes_ = binary_list_to_byte(rgb_to_binary_string(sorted_rgb))
        self.current_size += len(bytes_)
        print(self.size_of_file, self.current_size)
        while self.current_size > self.size_of_file:
            bytes_ = bytes_[:-1]
            self.current_size -= 1
        print(len(bytes_))
        with open(f'output/{self.filename}', 'ab') as f:
            f.write(bytes_)

    def main(self):
        for i in natsorted(os.listdir('output_frames'), key=lambda y: y.lower()):
            print(i)
            self.extract_bytes_from_photos(i)


if __name__ == '__main__':
    private_num = 8
    obj2 = CreateImages('test.text', 'username', private_num)
    obj2.main()
