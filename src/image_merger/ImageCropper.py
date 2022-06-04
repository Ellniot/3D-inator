# Image Cropper
#
# - main idea is the following
#   - present a dialog to the user telling them to click the same locaion on each immage
#       - i.e. the left pupil, or closest point to camera
#   - present each image to user and record clicked location
#   - find maximum size of images where that point is in the same position for all
#       - calculate distance to top, bottom, left, and right of point for each image
#   - crop each image to fit smallest of those dimensions
#
from turtle import width
from PIL import Image
from tkinter import *
from PIL import ImageTk, Image
import os

# get dimensions of image that best fit user's window
# return both the new dimensions & scale used
# TODO - only works when user has only one scree
# TODO - pull out into utility class?
def getBestImageFitDims(img):

    tmp_tk = Tk()
    
    # get the screen width and height for ui resizing
    scr_width = tmp_tk.winfo_screenwidth()
    scr_height = tmp_tk.winfo_screenheight()

    tmp_tk.destroy()

    # get 90% of each screen dim so there's extra room
    scr_width_lim = scr_width * .9
    scr_height_lim = scr_height * .9

    # get the image size
    img_size = img.size

    # check if each dimension is greater than the limit
    #   reduce to fit if so
    width_scale = 1
    height_scale = 1
    # width
    if img_size[0] > scr_width_lim:
        # get the precent to multiply the image width by
        width_scale = scr_width_lim / img_size[0]
    if img_size[1] > scr_height_lim:
        height_scale = scr_height_lim / img_size[1]
    
    # scale the image by whichever is smaller
    if width_scale < height_scale:
        new_width = img_size[0] * width_scale
        new_height = img_size[1] * width_scale
        return tuple((int(new_width), int(new_height))), width_scale
    else:
        new_width = img_size[0] * height_scale
        new_height = img_size[1] * height_scale
        return tuple((int(new_width), int(new_height))), height_scale


def askUserForPoints(images):
    # resize the images to fit the screen
    img_best_fit_dims = []
    img_best_fit_scales = []
    resized_images = []
    for i in range(3): # assuming 3 images
        dims, scale = getBestImageFitDims(images[i])
        img_best_fit_dims.append(dims)
        img_best_fit_scales.append(scale)
        tmp_img = images[i].copy().resize(img_best_fit_dims[i])
        resized_images.append(tmp_img.copy())
    #print(img_best_fit_dims)
    #print(img_best_fit_scales)

    # promp the user with a message
    # "please click on the same point in all three images, ideally, the closest point to the camera"

    photo_points = []
    # show the user each of the three images
    for i in range(3): # assuming 3 images
        # create the tk frame
        user_click_tk = Tk()
        # create the canvas
        canvas = Canvas(user_click_tk, width=img_best_fit_dims[i][0], height=img_best_fit_dims[i][1])
        canvas.pack()
        # add the image
        img=ImageTk.PhotoImage(resized_images[i])
        canvas.create_image(0, 0, image=img, anchor="nw")
        # create the click listener
        def callback(event):
            # dividing each point by the scale used get's the position on the full image (within a pixel or two)
            full_img_x_pos = int(event.x/img_best_fit_scales[i])
            full_img_y_pos = int(event.y/img_best_fit_scales[i])
            photo_points.append(tuple((full_img_x_pos, full_img_y_pos)))
            user_click_tk.destroy()
        canvas.bind("<Button-1>", callback)
        # wait for the click, add it to the photo_points list
        user_click_tk.mainloop()

    print(photo_points)
    return photo_points

# for each photo, find the distance from the clicked point to each side of the photo
# from this, find the max photo size, with the point in the same position for each photo
def findMaxDistancesFromPoints(dims, photo_points):

    all_px_to_edges = []
    for i in range(3): # assuming 3 images
        px_to_edges = [] # top, right, bottom, left 
        # subtract 1 from each dim to account for selected pixel
        max_wd = dims[i][0] - 1
        max_ht = dims[i][1] - 1
        # add distance to top
        px_to_edges.append(photo_points[i][1])
        # add distance to right
        px_to_edges.append(max_wd - photo_points[i][0])
        # add distance to bottom
        px_to_edges.append(max_ht - photo_points[i][1])
        # add distance to left
        px_to_edges.append(photo_points[i][0])
        # add the list to main list
        all_px_to_edges.append(px_to_edges.copy())
    print(all_px_to_edges)
    
    # find min for each direction
    max_px_each_dir = []
    for i in range(4):
        max_px_each_dir.append(min(all_px_to_edges[0][i], all_px_to_edges[1][i], all_px_to_edges[2][i]))
    print(max_px_each_dir)
    return max_px_each_dir, all_px_to_edges

# calculate the two points for each image that surround the smaller cropped image
def findCropBoxes(dims, max_px_each_dir, all_px_to_edges):
    # for each image
        # for each dir
            # if dir from point to edge > max px
                # get difference (ammount to crop out in that dir)
    all_px_by_dir_to_crop = []
    for img_px_to_edges in all_px_to_edges:
        excess_px_each_dir = []
        for i in range(4): # 4 directions, top, right, bottom, left
            if img_px_to_edges[i] > max_px_each_dir[i]:
                excess_px_each_dir.append(img_px_to_edges[i] - max_px_each_dir[i])
            else:
                excess_px_each_dir.append(0)
        all_px_by_dir_to_crop.append(excess_px_each_dir.copy())
    print(all_px_by_dir_to_crop)

    # get the coordinates from the image using the pixels to be cropped
    crop_coords = []
    for i in range(3): # assuming 3 images
        # (x1,y1), (x2,y2)
        # first coord set is elm 3, elm 0
        first_coord = tuple((all_px_by_dir_to_crop[i][3], all_px_by_dir_to_crop[i][0]))
        # second coord set is dim x - elm 1, dim x - elm 2
        x2 = dims[i][0] - all_px_by_dir_to_crop[i][1]
        y2 = dims[i][1] - all_px_by_dir_to_crop[i][2]
        second_coord = tuple((x2, y2))
        crop_coords.append([first_coord, second_coord])
    print(crop_coords)
    return crop_coords

def cropImages(images):

    photo_points = askUserForPoints(images)
    
    dims = []
    for img in images:
        dims.append(img.size)
    print(dims)

    max_px_each_dir, all_px_to_edges = findMaxDistancesFromPoints(dims, photo_points)

    crop_coords = findCropBoxes(dims, max_px_each_dir, all_px_to_edges)
    
    cropped_images = []
    for i in range(3): # assuming 3 images
        x1 = crop_coords[i][0][0]
        y1 = crop_coords[i][0][1]
        x2 = crop_coords[i][1][0]
        y2 = crop_coords[i][1][1]
        print((x1, y1), (x2, y2))
        cropped_images.append(images[i].crop((x1, y1, x2, y2)))
    return cropped_images

def test():

    img_1_path = "res/1.png"
    img_2_path = "res/2.png"
    img_3_path = "res/3.png"

    img1 = Image.open(img_1_path)
    img2 = Image.open(img_2_path)
    img3 = Image.open(img_3_path)

    images = [img1, img2, img3]
    cropped_images = cropImages(images)

    for i in range(3): # because this test has 3 images
        cropped_images[i].save("res/cropped/" + str(i) + "_cropped.png")

if (__name__) == "__main__":
    test()