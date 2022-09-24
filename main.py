import argparse
import os
import cv2
from util import create_dir


def sqaure_img(img_path, size=None, color=(255, 255, 255)):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    old_size = img.shape[:2]  # old_size is in (height, width) format

    if size:
        desired_size = size
    else:
        desired_size = max(old_size)

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    # new_size should be in (width, height) format
    img = cv2.resize(img, (new_size[1], new_size[0]))
    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return new_img


parser = argparse.ArgumentParser(description="Turn a landscape or portrait image to a square")
parser.add_argument("--path", type=str, default="./in/", help="Path to image or directory containing images or subdirectory of images")
parser.add_argument("--loop", dest='loop', action='store_true', help="If the directory has sub directories then use this")
parser.add_argument("--out", type=str, default="export", help="Name for the output folder")
parser.add_argument("--size", type=int, default=None, help="Set desired size for image, default: None")
parser.add_argument("--color", type=int, default=None, help="Color of the border, default: 255 255 255", nargs="+")
parser.set_defaults(loop=False)
args = parser.parse_args()

path = args.path
loop = args.loop
out = args.out
size = args.size

if args.color is None:
    color = (255,255,255)
else:
    color = tuple(args.color)

in_dir = os.path.join(os.getcwd(), path)

if not os.path.exists(path) or not os.path.exists(in_dir):
    print("error: invalid --path provided")
    exit(1)

if os.path.isfile(path):
    img_name = os.path.basename(path)
    out_dir = os.path.join(os.path.dirname(path), out)
    create_dir(out_dir)

    img_out = os.path.join(out_dir, img_name)
    img = sqaure_img(path, size=size, color=color)
    cv2.imwrite(img_out, img)

    print("image saved to:", img_out)
    exit(0)

if not loop:
    print("please set --loop if you want to loop through all images in the directory")
    exit(1)

for root, dirs, files in os.walk(in_dir, topdown=False):
    out_dir = os.path.join(root, out)

    if os.path.basename(root) == os.path.basename(out_dir):
        continue

    create_dir(out_dir)

    for img_name in files:
        img_path = os.path.join(root, img_name)
        img_out = os.path.join(out_dir, img_name)

        img = sqaure_img(img_path, size=size, color=color)
        cv2.imwrite(img_out, img)

        print(img_out)