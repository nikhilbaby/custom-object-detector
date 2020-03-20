# Imports
import os
import glob
import progressbar
import cv2

import config


# Check if the raw_images directory exists
if not os.path.exists(config.RAW_IMAGES_DIR):
    print("Raw images directory: No")
else:
    print("Raw images directory: Yes")


if not os.path.exists(config.RESIZED_IMAGES_DIR):
    print("Resized images directory: No")
    os.makedirs(config.RESIZED_IMAGES_DIR)
    print("Create resized images directory: Yes")

else:
    print("Resized images directory: Yes")


# Get the names of all files in the raw_images directory
file_names = glob.glob(os.path.join(config.RAW_IMAGES_DIR, "*.{}".format(config.IMAGE_EXTENSION)))
print("Files in raw images directory: {}".format(len(file_names)))

bar = progressbar.ProgressBar(maxval=len(file_names), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
print("Resizing images:-")

#  Loop through the images and resize the images
for i, filename in enumerate(file_names):
    img = cv2.imread(filename)
    img_resized = cv2.resize(img, config.RESIZE_DIMS)
    new_filename = "{}.{}".format(str(i), config.IMAGE_EXTENSION )
    new_filepath = os.path.join(config.RESIZED_IMAGES_DIR, new_filename)
    cv2.imwrite(new_filepath, img_resized)
    bar.update(i + 1)
bar.finish()

print("Saved images to: {}".format(config.RESIZED_IMAGES_DIR))













