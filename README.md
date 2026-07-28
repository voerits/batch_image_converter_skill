# A skill for converting image style in batches.

### Features

1. Convert images to whatever style you want.

2. Conversion is in a batch, and it preserves the original file directory structure as your input image directories.

3. Very easy to set off. A simple sentence in your Codex terminal and everything is done.

### How to use it

Very easy! Prompt in your Codex terminal:

*Load the skill in ./skills/batch-image-converter, run this batch image converter. The image folder is [Path-to-images]. The conversion's requirement text file is [Path-to-conversion-requirement-text].*

And let your Codex run it!


### What it does

Given a folder containing images, it generates new images which have converted the original images' style as to user's illustrations. This conversion has the features below:

1. The output images are organized in a new folder, which preserves the same directory structure as the original image folder. The names of the sub-directories and image files are also preserved. However, the files other than image files are ignored and are not included in the output folder.

eg. 

    original folder:
    image_folder/
        |____subfolder_1/
            |____subsubfolder_1/
                |____image1.png
                |____image2.jpg
                |____image3.jpeg              
            |____text1.txt
            |____image4.jpg
            |____subsubfolder_2/
                |____video.mp4
                |____image5.jpg
        |____subfolder_2/
            |____subsubfolder_3/
                |____subsubfolder_1/
                    |____image6.png
            |____image7.jpg

    new folder:
    image_folder_converted/
        |____subfolder_1/
            |____subsubfolder_1/
                |____image1.png
                |____image2.jpg
                |____image3.jpeg
            |____image4.jpg
            |____subsubfolder_2/
                |____image5.jpg
        |____subfolder_2/
            |____subsubfolder_3/
                |____subsubfolder_1/
                    |____image6.png
            |____image7.jpg

2. The conversion is conducted by AI agent per image file. The requirement for the conversion is provided by user. 

eg.:

    Convert the provided image into a simple cartoon illustration.

    Requirements:
    1. Keep only the main object from the original image. Remove all other objects, clutter, shadows, textures, props, labels, backgrounds, and unnecessary details.
    2. Draw the main object with clean, simplified black outlines.
    3. Use bright, simple colors that make the object easy for a child to recognize and distinguish.
    4. Preserve the object’s basic shape, orientation, and key identifying features from the original image.
    5. Place the cartoon object centered on a plain white background.
    6. Do not add any text, decorations, extra objects, or scenery.
    7. Has a size of 1280 x 1280 pixels.


### Note

since the image conversion is executed by your agent, there is possibility that a few of the images are not perfectly converted to what you want. You are recommended to check the converted image outputs, and select the few unsatisfied images for a re-run.