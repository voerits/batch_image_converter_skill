import argparse

import io
from pathlib import Path

from PIL import Image

import utils.retrieve as retrieve
import utils.toagent as toagent
import utils.generate as generate


if __name__ == "__main__":
    # Receive user inputs for image and prompt file directory paths
    parser = argparse.ArgumentParser()

    parser.add_argument('--images', type=str, default="./assets/images")
    parser.add_argument('--prompt', type=str, default="./assets/prompt.txt")
    parser.add_argument('--imgformats', nargs='+', type=str, default=['JPG','PNG','JPEG'])

    args = parser.parse_args()
    kwarg_dict = vars(args)

    path_img = Path(kwarg_dict['images'])
    prompt_file = Path(kwarg_dict['prompt'])
    img_formats = [x.lower() for x in kwarg_dict['imgeformats']]

    # Load images
    image_file_list = retrieve.retrieve_file_lists(path_img, img_formats)

    # Load prompt
    with prompt_file.open(mode='r') as f:
        prompt = f.read()

    print(f"User prompt: {prompt}")

    # Make the new image folder
    save_dir = retrieve.make_new_folder(path_img)

    # Generate converted image for each image
    for img_fp in image_file_list:
        ## Retrieve image in binary format bytes
        img_io = retrieve(img_fp)
        img_format = img_fp.name.strip().split('.')[-1]

        prompt = generate.make_prompt(img_io, img_format, prompt)

        ## Interact with agent
        img_converted_io = generate.convert_by_agent(prompt)
        img_converted = Image.open(img_converted_io)

        ## Save image
        image_path_relative = img_fp.relative_to(path_img)
        save_path = save_dir / image_path_relative
        generate.save_image(img_converted, img_format, save_path)


