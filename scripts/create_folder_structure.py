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
        help='directory with input masks'
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

    dir_create('../Images/Train_test_split/3_dias/Normais/train_imgs')
    dir_create('../Images/Train_test_split/3_dias/Normais/train_masks')
    dir_create('../Images/Train_test_split/3_dias/Normais/val_imgs')
    dir_create('../Images/Train_test_split/3_dias/Normais/val_masks')

    image_names = [f for f in os.listdir(args.base_image_dir) if f.endswith(".png")]
    
    print(image_names)
    
    X, Y = train_test_split(image_names, test_size=0.3)

    train_imgs_paths = []
    train_masks_paths = []
    for image_name in X:
        train_imgs_paths.append(os.path.join(args.base_image_dir, image_name))
        train_masks_paths.append(os.path.join(args.base_segmentation_dir, image_name))

    val_img_paths = []
    val_masks_paths = []
    for image_name in Y:
        val_img_paths.append(os.path.join(args.base_image_dir, image_name))
        val_masks_paths.append(os.path.join(args.base_segmentation_dir, image_name))

    for train_img_path, train_mask_path in zip(train_imgs_paths,train_masks_paths):
        shutil.copy(train_img_path, '../Images/Train_test_split/3_dias/Normais/train_imgs')
        shutil.copy(train_mask_path, '../Images/Train_test_split/3_dias/Normais/train_masks')

    for val_img_path, val_mask_path in zip(val_img_paths,val_masks_paths):
        shutil.copy(val_img_path, '../Images/Train_test_split/3_dias/Normais/val_imgs')
        shutil.copy(val_mask_path, '../Images/Train_test_split/3_dias/Normais/val_masks')

if __name__ == "__main__":
    main()

