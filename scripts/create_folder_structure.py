import os
import argparse
import shutil
from sklearn.model_selection import train_test_split

def parse_args():
    parser = argparse.ArgumentParser(
        fromfile_prefix_chars='@',
        description='Convert CVAT XML annotations to contours'
    )
    
    parser.add_argument(
        '--base-image-dir', metavar='DIRECTORY', required=True,
        help='directory with input images'
    )
    
    parser.add_argument(
        '--base-segmentation-dir', metavar='DIRECTORY', required=True,
        help='directory with input images'
    )

    return parser.parse_args()

def dir_create(path):  
    if (os.path.exists(path)) and (os.listdir(path) != []):
        shutil.rmtree(path)
        os.makedirs(path)
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    
    args = parse_args()

    print(args)

    dir_create('./train_images')
    dir_create('./train_segmentation')
    dir_create('./val_images')
    dir_create('./val_segmentation')

    image_names = [f for f in os.listdir(args.base_image_dir) if f.endswith(".png")]

    X, Y = train_test_split(image_names, test_size=0.3)

    train_paths = []
    train_seg_paths = []
    for image_name in X:
        train_paths.append(os.path.join(args.base_image_dir, image_name))
        train_seg_paths.append(os.path.join(args.base_segmentation_dir, image_name))

    test_paths = []
    test_seg_paths = []
    for image_name in Y:
        test_paths.append(os.path.join(args.base_image_dir, image_name))
        test_seg_paths.append(os.path.join(args.base_segmentation_dir, image_name))

    for train_path, train_seg_path in zip(train_paths,train_seg_paths):
        shutil.copy(train_path, 'train_images')
        shutil.copy(train_seg_path, 'train_segmentation')

    for test_path, test_seg_path in zip(test_paths,test_seg_paths):
        shutil.copy(test_path, 'val_images')
        shutil.copy(test_seg_path, 'val_segmentation')

if __name__ == "__main__":
    main()

