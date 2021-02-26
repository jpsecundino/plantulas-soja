import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np

seq = iaa.Sequential([
    iaa.Crop(px=(0, 16)), # crop images from each side by 0 to 16px (randomly chosen)
    iaa.Fliplr(0.5), # horizontally flip 50% of the images
    iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
])

def augment_seg( img , seg  ):
	
	aug_det = seq.to_deterministic() 
	image_aug = aug_det.augment_image( img )

	segmap = ia.SegmentationMapOnImage( seg , nb_classes= np.max(seg)+1 , shape=img.shape )
	segmap_aug = aug_det.augment_segmentation_maps( segmap )
	segmap_aug = segmap_aug.get_arr_int()

	return image_aug , segmap_aug

from keras_segmentation.models.unet import vgg_unet

model = vgg_unet(n_classes=51 ,  input_height=4608, input_width=3456)

model.train( 
    train_images =  "TrainTestSplit/train_images",
    train_annotations = "TrainTestSplit/train_segmentation",
    checkpoints_path = "Checkpoints/vgg_unet_1" , epochs=5
)