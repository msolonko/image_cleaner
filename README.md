# Image Cleaner
This Image Cleaner tool, inspired by a PyImageSearch tutorial, goes through a directory of images and deletes all blurry images as well as all duplicates. This is meant to be convenient for directories with hundreds or thousands of images when manually inspecting each one would take too long.

## Usage
Download the Python file and optionally the test image folder

You will need OpenCV and Imutils installed to run the Python file. You can follow the following directions in your terminal where we will create a virtual environment for you to run this file:

If you don't have `virtualenv` installed for Python, run
``` bash
pip install virtualenv
```

Make a virtual environment:
``` bash
python -m venv virt
```

To activate the environment, on Windows run:
``` bash
virt\Scripts\activate
```

And on Linux or Mac run:
``` bash
source virt/bin/activate
```

To install the necessary pip packages into the environment, run:
``` bash
pip install -r requirements.txt
```

Finally, to run the Python application, run:
``` bash
python clean_images.py -i test_images
```

After running the above command on `test_images`, the directory should only have unique and clear images left. Please use with caution with your own images.

Replace `test_images` with your own path. Also, the blurriness detection is not perfect, so there might be some unnecessary removals or undeleted blurry images. Check your recycling bin to ensure nothing of value was deleted (much faster than going image by image). Enjoy!
