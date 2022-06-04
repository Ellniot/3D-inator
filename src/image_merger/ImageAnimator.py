from PIL import Image

# TODO - add check for invalid filename chars

# filename should NOT have extension
def animateAndSaveGif(images, file_name):

    # organise the images so they go 1,2,3,2
    images.append(images[1])

    # save the gif
    images[0].save(file_name + '.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=120, loop=0)

    

def test():
    img_1_path = "res/normalized/0_colors_normalized.png"
    img_2_path = "res/normalized/1_colors_normalized.png"
    img_3_path = "res/normalized/2_colors_normalized.png"

    # img_1_path = "res/cropped/0_cropped.png"
    # img_2_path = "res/cropped/1_cropped.png"
    # img_3_path = "res/cropped/2_cropped.png"

    img1 = Image.open(img_1_path)
    img2 = Image.open(img_2_path)
    img3 = Image.open(img_3_path)

    images = [img1, img2, img3]
    animateAndSaveGif(images, "Jonny-Gray-Gus-in-Car-normalized")

if (__name__) == "__main__":
    test()