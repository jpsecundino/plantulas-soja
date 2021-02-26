image_dir = ""
xml_dir = ""
segmentation_dir = ""


run:
	python3 jpgToPng.py --image-dir $(image_dir)
	python3 prepare_xml.py --cvat-xml $(xml_dir)
	python3 cvat_parser.py --image-dir $(image_dir) --cvat-xml $(xml_dir) --output-dir $(segmentation_dir) --scale-factor 1
	# sudo python3 create_folder_structure.py --base-image-dir=$(image_dir) --base-segmentation-dir=$(segmentation_dir)


