import numpy as np
import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, help="Input video directory to be filtered")
parser.add_argument("--output_dir", type=str, help="Output video directory")
parser.add_argument("--mask_path", type=str, help="path of mask file")
args = parser.parse_args()


input_dir = args.input_dir
output_dir = args.output_dir
mask_path = args.mask_path
if not os.path.exists(output_dir):  
    os.makedirs(output_dir)

mask = cv2.imread(mask_path)
zeros = np.zeros([4000, 1000, 3], dtype=np.uint8)
mask = np.concatenate([zeros, mask, zeros], axis=1)
mask[mask<=127] = 0
mask[mask>127] = 1

for i in range(1, 73):
    img = cv2.imread(os.path.join(input_dir, "frame_%04d"%i+".png"))
    _ = cv2.imwrite(os.path.join(output_dir, "frame_%04d"%i+".png"), img*mask)
    print("Process %d " % i)

