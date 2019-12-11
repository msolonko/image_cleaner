from imutils import paths
import argparse
import cv2
from send2trash import send2trash
import hashlib




# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
    help="path to input directory of images")

# adjust the value below to tweak blurriness levels that trigger removal
ap.add_argument("-t", "--threshold", type=float, default=50.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

PRINT_UPDATES = False

def run():
    global PRINT_UPDATES
    print("[INFO] Starting cleaning in directory " + args["images"])
    print("[INFO] Removing blurriness...")

    
    num_paths = sum(1 for _ in paths.list_images(args["images"])) # calculates the number of paths

    if num_paths > 50: # only prints updates if the directory is large
        PRINT_UPDATES = True
    i = 0
    for imagePath in paths.list_images(args["images"]):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # low values indicate blurriness
        fm = variance_of_laplacian(gray)
        if fm < args["threshold"]:
            send2trash(imagePath)

        # update printing
        if i%10 == 0:
            print_updates(i, num_paths)
        i += 1

    print("[INFO] Blurry images removed")
    print("[INFO] Removing duplicates...")

    # gets a list of paths to delete
    duplicates = get_dups(paths.list_images(args["images"]), paths.list_images(args["images"]))
    for path in duplicates:
        send2trash(path)

    print("[INFO] Done!")


def hashfile(path, blocksize = 65536):
    # generates unique hash for each unique image
    afile = open(path, 'rb')
    hasher = hashlib.sha512()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def variance_of_laplacian(image):
    # calculates variance score to determine how blurry an image is
    return cv2.Laplacian(image, cv2.CV_64F).var()

def get_dups(paths1, paths2):
    dups = {}
    dup_paths_list = []
    num_paths = sum(1 for _ in paths2)
    i = 0
    for imagePath in paths1:
        # Calculate hash
        file_hash = hashfile(imagePath)
        
        # if hash already exists, we found a duplicate
        if file_hash in dups:
            dup_paths_list.append(imagePath)
        else:
            # adds the first occurence of hash to dictionary
            dups[file_hash] = imagePath
        if i%10 == 0:
            print_updates(i, num_paths)
        i += 1
    return dup_paths_list

def print_updates(i, length):
    # determines percent that has been done
    if PRINT_UPDATES:
        div = int(i / length * 100)
        print(str(div) + "% done...")

run()
