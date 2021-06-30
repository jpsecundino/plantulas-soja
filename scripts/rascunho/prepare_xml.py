
import argparse
import os
from shutil import copyfile

def parse_args():
    parser = argparse.ArgumentParser(
        fromfile_prefix_chars='@',
        description='Convert CVAT XML annotations to contours'
    )
    
    parser.add_argument(
        '--cvat-xml', metavar='FILE', required=True,
        help='input file with CVAT annotation in xml format'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    

    fin = open(args.cvat_xml, "rt")
    
    #output file to write the result to
    fout_path = args.cvat_xml.split('.')[0] + '_temp.xml'
    
    fout = open(fout_path, "wt")
    
    #for each line in the input file
    for line in fin:
        #read replace the string and write to output file
        fout.write(line.replace('jpg', 'png'))
    
    #close input and output files
    fin.close()
    fout.close()    

    copyfile(fout_path, args.cvat_xml)

    os.remove(fout_path)

if __name__ == "__main__":
    main()
