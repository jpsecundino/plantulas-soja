from PIL import Image
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        fromfile_prefix_chars='@',
        description='Convert CVAT XML annotations to contours'
    )
    
    parser.add_argument(
        '--image-dir', metavar='DIRECTORY', required=True,
        help='directory with input images'
    )
    

    return parser.parse_args()


def main():
    
    args = parse_args()
    print(args)

    image_names = [f for f in os.listdir(args.image_dir)]

    image_paths = []
    for image_name in image_names:
        image_paths.append( os.path.join(args.image_dir, image_name ))

    print(image_paths)

    for image_path in image_paths:
        im1 = Image.open(image_path)
        im1.save(image_path.split(".")[0] + '.png')

    files_in_directory = os.listdir(args.image_dir)
    filtered_files = [file for file in files_in_directory if file.endswith(".jpg")]
    for file in filtered_files:
        path_to_file = os.path.join(args.image_dir, file)
        os.remove(path_to_file)    

if __name__ == "__main__":
    main()
