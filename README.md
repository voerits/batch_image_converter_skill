# A skill for converting image style in batches.

### What it does

Given a folder containing images, it generates new images which have converted the original images' style as to user's illustrations. This convertion has the features below:

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

2. The convertion is conducted by AI agent per image file. The requirement for the convertion is provided by user. 

eg.:

"Add white cloud and blue sky in each of these images."

"Make these images cartoon-like."