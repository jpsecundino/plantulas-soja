# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
# import dicttoxml


# %%
IMGS_PATH = "../Images/3_dias/Normais/images/"
# MASKS_PATH = "../Images/3_dias/Normais/masks/"
IMGS_BOUND_PATH = "../Images/3_dias/Normais/images_bound"
# MASKS_BOUND_PATH = "../Images/3_dias/Normais/masks_cut"

def imshow_components(labels):
    # Map component labels to hue val
    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0
    plt.figure(figsize=(50, 50))
    plt.imshow(labeled_img)
    plt.show()

def find_extremes(img):
    north = [0, 0]
    south = [0, 0]
    east =[0, 0]
    west = [0, 0]
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] == True:
                if north == [0,0] or west == [0,0]:
                    north = [y,x]
                    west = [y,x]
                if y < north[0]:
                    north = [y,x]
                if x > east[1]:
                    east = [y,x]
                if y > south[0]:
                    south = [y,x]
                if x < west[1]:
                    west = [y,x]
    return north, south, east, west
                    
def draw_box(img, north, south, east, west):
    cv2.line(img, (west[1], south[0]), (east[1], south[0]), (255, 0, 0), 5, 1)
    cv2.line(img, (west[1], north[0]), (east[1], north[0]), (255, 0, 0), 5, 1)
    cv2.line(img, (west[1], south[0]), (west[1], north[0]), (255, 0, 0), 5, 1)
    cv2.line(img, (east[1], north[0]), (east[1], south[0]), (255, 0, 0), 5, 1)
    plt.figure(figsize=(50, 50))
    plt.imshow(img)
    plt.show()

def get_image(img_name):
    image_path = os.path.join(IMGS_PATH, img_name)
    image = cv2.imread(image_path,1)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    info = {
        "path": image_path,
        "boxes":[]
    }

    return image, info


def get_image_pair(img_name):
    image_path = os.path.join(IMGS_PATH, img_name)
    mask_path = os.path.join(MASKS_PATH, img_name)
    image = cv2.imread(image_path,1)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask = cv2.imread(mask_path,0)
    return image, mask

def pre_process(image):
    kernel = np.ones((2,2),np.uint8)
    
    opening_img = cv2.morphologyEx(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), cv2.MORPH_OPEN, kernel)
    
    th,thresh_img = cv2.threshold(opening_img, 50, 255, cv2.THRESH_TOZERO)
    
    

    num_components, components = cv2.connectedComponents(thresh_img, connectivity=8)
    print("Number of components:", num_components)

    
#     plt.figure(figsize=(50, 50))
#     plt.imshow(thresh_img, cmap='gray')
#     plt.show()
    
    return num_components, components, thresh_img

def save_image(image_name, image, idx):
    if image is None:
        return
    if image.shape[0] < 40 or image.shape[1] < 40:
        return
    if not os.path.exists(IMGS_CUT_PATH):
        os.makedirs(IMGS_CUT_PATH)
    
    img_path = os.path.join(IMGS_CUT_PATH, image_name.split('.')[0] + "_" + str(idx) + "." + image_name.split('.')[1])
    print(img_path)
    cv2.imwrite(img_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def save_images(image_name, image, mask, idx):
    if image is None or mask is None:
        return
    if image.shape[0] < 40 or image.shape[1] < 40:
        return
    if not os.path.exists(IMGS_CUT_PATH):
        os.makedirs(IMGS_CUT_PATH)
    if not os.path.exists(MASKS_CUT_PATH):
        os.makedirs(MASKS_CUT_PATH)
    
    img_path = os.path.join(IMGS_CUT_PATH, image_name.split('.')[0] + "_" + str(idx) + "." + image_name.split('.')[1])
    mask_path = os.path.join(MASKS_CUT_PATH, image_name + image_name.split('.')[0] + "_" + str(idx) + "." + image_name.split('.')[1])
    print(img_path, mask_path)
    cv2.imwrite(img_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.imwrite(mask_path, cv2.cvtColor(mask, cv2.COLOR_RGB2BGR))

def grid_image(image):
    
    # Grid lines at these intervals (in pixels)
    # dx and dy can be different
    dx, dy = 864, 450
    
    if image.shape[0] > image.shape[1]:
        dx, dy = dy, dx

    # Custom (rgb) grid color
    grid_color = [255,255,255]

    # Modify the image to include the grid
    image[:,::dy,:] = grid_color
    image[::dx,:,:] = grid_color

def bound_images_func(image_names, hasMask = False):
    for image_name in image_names:
        if hasMask is True:
            image, mask = get_image_pair(image_name)
        else:
            image, info = get_image(image_name)

        print(image.shape)

        num_components, components, processed_image = pre_process(image)   
        
        # imshow_components(components)
        
        
        for component_idx in range(1, num_components - 1):
            if np.count_nonzero(components == component_idx) < 100:
#                 print(np.count_nonzero(components == component_idx))
                continue
            component = components[:,:] == component_idx
            north, south, east, west = find_extremes(component)
            if abs(north[0] - south[0]) < 40 or abs(east[1] - west[1]) < 40:
                print("Corte pequeno demais")
                continue
            
            box = {
                "xmax":south[0],
                "xmin":north[0],
                "ymax":east[1],
                "ymin":west[1],
            }

            info["boxes"].append(box)
         
        a_file = open(f"{os.path.join(IMGS_BOUND_PATH, image_name)}.pkl", "wb")
        pickle.dump(dictionary_data, a_file)
        a_file.close()


# %%
image_names = os.listdir(IMGS_PATH)

import multiprocessing 
  
# Yield successive n-sized 
# chunks from l. 
def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

inputs = list(divide_chunks(image_names, 2)) 

processes = list()

for input in inputs:
    x = multiprocessing.Process(target=bound_images_func, args=(input, False,))
    processes.append(x)
    x.start() 




# %%



# %%



# %%


    





# %%



# %%



# %%



# %%



# %%



# %%



