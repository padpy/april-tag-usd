#!/usr/bin/env python3

import os
import argparse
from PIL import Image
from PIL import ImageDraw, ImageFont
import re
# from pxr import Usd

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
    description='A script to convert pre-generated apriltag .png files into into USD models',
    epilog='Example: "python tag_to_usd.py"'
)
parser.add_argument(
    '-f', '--tag-folder', type=str, required=False, default='tags/tag36h11/',
    help='The path to the AprilTag .png files'
)
parser.add_argument(
    '-o', '--output', type=str, required=False, default='tag',
    help='Output file name template. FILENAME -> FILENAME_00000.png'
)
parser.add_argument(
    '-n', '--num-tags', type=int, required=False, default=1, dest="num_tags",
    help='Number of tags to generate'
)
parser.add_argument(
    '-p', '--pixels', type=int, required=False, default=512, dest="pixels",
    help='Number of pixels (N) in the output image (NxN)'
)
parser.add_argument(
    '-t', '--target', type=str, required=False, default='tag.usd',
    help='Output file name to inject the AprilTag models. If none is provided, then one will be generated.'

)

def create_resized_png(tag_folder, out_file, num_bits, hamming_distance, i, pixels):
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with Image.open(os.path.join(tag_folder, f'tag{num_bits}_{hamming_distance}_{i:05}.png'), 'r') as im:
        im = im.resize((pixels,pixels), Image.NEAREST)
        img_draw = ImageDraw.Draw(im)
        img_draw.text((236,465), f'{i:02}', fill=(0,0,255), font=ImageFont.truetype("FreeMono.ttf", 40))
        im.save(os.path.join(output_dir, f'{out_file}_{i:05}.png'))

def main():
    args = parser.parse_args()
    tag_folder = args.tag_folder
    output = args.output
    num_tags = args.num_tags
    pixels = args.pixels

    # The naming of tag families follows the format [NUMBITS]h[HAMMINGDISTANCE] - eg 36h11
    num_bits, hamming_distance = re.findall(r'\d+', tag_folder)

    # Resize images for textures
    for i in range(num_tags):
        create_resized_png(tag_folder, output, num_bits, hamming_distance, i, pixels)



if __name__ == "__main__":
    main()
