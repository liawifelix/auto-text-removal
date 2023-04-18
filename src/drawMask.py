import cv2
import numpy as np
import argparse
import os
import glob


def drawMask(points, image):
    points = np.array(points)
    cv2.fillPoly(image, [points], color=(255, 255, 255))
    return image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw Mask')
    parser.add_argument('--coor_input_folder', type=str)
    parser.add_argument('--input_folder', type=str)
    parser.add_argument('--mask_output_folder', type=str)
    parser.add_argument('--radius', type=int, default=0)
    parser.add_argument('--output_real_image', type=bool, default=False)
    args = parser.parse_args()

    folder_path = args.input_folder
    file_pattern = "*"
    files = glob.glob(os.path.join(folder_path, file_pattern))
    for file in files:
        img = cv2.imread(file)
        img_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        file_name_ext = file.split("/")[1]

        file_name = file_name_ext.split(".")[0]
        ext = file_name_ext.split(".")[1]
        gt_file = f"{args.coor_input_folder}/res_{file_name}.txt"

        radius = args.radius
        row, col, channel = img.shape

        with open(gt_file, "r", encoding="utf-8") as f:
            for line in f:
                points = list(map(lambda x: int(x), line.strip().split(",")))
                xy1 = (max(points[0] - radius, 0), max(points[1] - radius, 0))
                xy2 = (min(points[2] + radius, col-1), max(points[3] - radius, 0))
                xy3 = (min(points[4] + radius, col-1), min(points[5] + radius, row-1))
                xy4 = (max(points[6] - radius, 0), min(points[7] + radius, row-1))
                points = np.array([xy1, xy2, xy3, xy4])

                img_mask = drawMask(points, img_mask)
        
        ext = 'png'
        cv2.imwrite(f"{args.mask_output_folder}/{file_name}_mask.{ext}", img_mask)
        
        if args.output_real_image:
            cv2.imwrite(f"{args.mask_output_folder}/{file_name}.{ext}", img)