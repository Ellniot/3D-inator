# for adding util module dir to path
import sys

# since .copy() on a 2d list doesnt create new inner lists
import copy

from PIL import Image
import torchvision.transforms as transforms

# sets how intense the changes are
COLOR_INTENSITY_MULTIPLIER = 2

# local imports
#TODO - update this once tests are moved out of this file
# update path to have /src dir in addition to /src/image_merger
print(sys.path)
cwd = sys.path[0]
split_cwd = cwd.split("\\")
del split_cwd[-1]
new_cwd = "\\".join(split_cwd)
sys.path.append(new_cwd)
try:
    from util.MatrixManiplulation import mirror_matrix
except:
    print("no import")

# takes the average value for all pixes
# returns array of [r, g, b] averages
def averageColors(img):
    pixels = img.load()
    totals = [0.0, 0.0, 0.0]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = pixels[x,y]
            for c in range(3):
                totals[c] += color[c] ** 2.2 # this is apparently gamma? not sure. idk if it matters since it's constant
    count = img.size[0] * img.size[1]
    color = [int(round((totals[c] / count) ** (1/2.2))) for c in range(3)]
    return color


#adjust each image to fit average
def adjustImageColors(img, old_rgb, avg_rgb):
    print(str(old_rgb))
    print(str(avg_rgb))
    # get the changes as value from 0-1 for each channel
    new_rgb = []
    for channel in range(3):
        # calculate the channel %
        old_channel_percent = old_rgb[channel]/256
        avg_channel_percent = avg_rgb[channel]/256
        # calculate the percent change
        percent_change = avg_channel_percent - old_channel_percent
        new_rgb.append(1 + (COLOR_INTENSITY_MULTIPLIER*percent_change))
    print(new_rgb)
    #convsersion matrix info https://www.geeksforgeeks.org/python-channel-drop-using-pillow/?ref=lbp
    conversion_matrix = (new_rgb[0], 0, 0, 0, 0, new_rgb[1], 0, 0, 0, 0, new_rgb[2], 0)
    print(conversion_matrix)
    return img.convert("RGB", conversion_matrix)


# takes three images (as ???)
# returns the three images with normalized colors

def normalizeColors(images):
    # check if there are not 3 images in the set
    if len(images) != 3:
        raise Exception("Exactly 3 images must be sent to normalizeColors(), recieved: " +len(images))

    # figure out average for each r, g, and b
    # then adjust each pixel in each image to match
    images_rgb_avg_lst = []
    for img in images:
        avg = averageColors(img)
        images_rgb_avg_lst.append(avg)
    print("Avg [[r, g, b], ...] for each image: " + str(images_rgb_avg_lst))

    # flip the array on it's diagonal to change list of image's colors
    # to list of colors for each image
    rgb_avg_lst = copy.deepcopy(images_rgb_avg_lst)
    rgb_avg_lst = mirror_matrix(rgb_avg_lst, 3) # assignment unneccesarry
    print("Avg [[r,r,r], [g,g,g] [b,b,b]] for each image: " + str(rgb_avg_lst))

    # average each row
    rgb_avgs = []
    for row in rgb_avg_lst:
        total = 0
        for i in row:
            total = total + i
        # divide, remove remainder
        # assuming 3 photos
        rgb_avgs.append(total//3)
    print("Overall Average [r, g, b]: " + str(rgb_avgs))

    color_corrected_images = []
    for i in range(3): # assuming 3 photos
        color_corrected_images.append(adjustImageColors(images[i], images_rgb_avg_lst[i], rgb_avgs))
    return color_corrected_images


def test():

    img_1_path = "res/cropped/0_cropped.png"
    img_2_path = "res/cropped/1_cropped.png"
    img_3_path = "res/cropped/2_cropped.png"

    img1 = Image.open(img_1_path)
    img2 = Image.open(img_2_path)
    img3 = Image.open(img_3_path)

    images = [img1, img2, img3]
    normalized_images = normalizeColors(images)

    for i in range(3): # because this test has 3 images
        normalized_images[i].save("res/normalized/" + str(i) + "_colors_normalized.png")


if (__name__) == "__main__":
    test()
