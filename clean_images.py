from imutils import paths
import argparse
import cv2
import os
 
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
    help="path to input directory of images")

# adjust the value below to tweak blurriness levels that trigger removal
ap.add_argument("-t", "--threshold", type=float, default=100.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

print("[INFO] Starting cleaning in directory " + args["images"])
print("[INFO] Removing blurriness...")

for imagePath in paths.list_images(args["images"]):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # low values indicate blurriness
    fm = variance_of_laplacian(gray)
    if fm < args["threshold"]:
        os.remove(imagePath)
        
print("[INFO] Blurry images removed")
print("[INFO] Removing duplicates...")
for imagePath1 in paths.list_images(args["images"]):
    for imagePath2 in paths.list_images(args["images"]):
        if imagePath1 != imagePath2:
            image1 = cv2.imread(imagePath1)
            image2 = cv2.imread(imagePath2)
            
            # checks for the same shape and if both images have not been deleted yet
            if image1 is not None and image2 is not None and image1.shape == image2.shape:
                difference = cv2.subtract(image1, image2)
                b, g, r = cv2.split(difference)
                
                # if the difference between two images is 0, they are identical
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    os.remove(imagePath2)
                    
print("[INFO] Done!")
        
