1. **retrieve.py** From the original folder (eg., `E:/original_folder/`), get a list of all the included images. This list lists the images' filenames, in the format of their complete absolute path. Eg., `E:/orginal_folder/dir1/dir2/dir3/image.jpg`

2. **retrieve.py** Make a new folder (make sure this folder does not exist) parallel to the original folder. This new folder is under the same parent directory of the original folder, and is named based on the original folder. Eg., `E:/converted_original_folder/` for `E:/original_folder/`.

3. **generate.py** Read the image path list. For each image:

a. **toagent.py** Send this image, together with the convertion illustration prompted by the user and the convertion command pre-defined by the script, to the AI agent that this skill is using.

b. **generate.py** Get the output converted image from the AI agent, and store it under the same folder structure, but under `converted_original_folder/` other than `original_folder/`.

4. (Optional) Output a .txt file visualizing the folder structure, together with the number of image files under each subfolder, not recursively.