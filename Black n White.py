from tkinter import Tk, Frame, Scale, Button, Label, IntVar, DoubleVar
from tkinter import filedialog as fd
import PIL.ImageTk
import PIL.ImageFilter
import PIL.Image

image = None
bw_image = None
has_opened = False


def convert_to_BW_pixels(image, buckets=100):
    pixels = list(image.getdata())
    return [pixel_value // buckets if pixel_value // buckets == 0 else 255 for pixel_value in pixels]


def BW(image, buckets, radius):
    width, height = image.size
    image = image.filter(PIL.ImageFilter.GaussianBlur(radius=radius))
    new_image = PIL.Image.new(mode="L", size=(
        width, height), color="white")
    new_image.putdata(convert_to_BW_pixels(image.convert("L"), buckets))
    return new_image


def resize(image):
    width, height = image.size

    if height > width:
        new_height = 400
        x = 400 / height
        new_width = width * x
    elif width > height:
        new_width = 400
        x = 400 / width
        new_height = height * x
    else:
        new_width = 400
        new_height = 400

    image = image.resize((round(new_width), round(new_height)),
                         PIL.Image.LANCZOS)
    return image


def show(image):
    display_photo = PIL.ImageTk.PhotoImage(resize(image))
    panel.configure(image=display_photo)
    panel.image = display_photo


def update_image(buckets, smoothness_radius):
    global has_opened
    global image
    global bw_image
    if has_opened:
        bw_image = BW(image, buckets, smoothness_radius)
        show(bw_image)


def save(image):
    save_image = fd.asksaveasfilename()
    if save_image:
        image.save(f"{save_image}.png", format="PNG")


def open_img(buckets, smoothness_radius):
    global has_opened
    global image
    global bw_image
    open_image = fd.askopenfilename()
    if open_image:
        has_opened = True
        image = PIL.Image.open(open_image)
        bw_image = BW(image, buckets, smoothness_radius)
        show(bw_image)


root = Tk()
root.title("Black n White")
root.minsize(400, 555)
root.maxsize(400, 555)

frame = Frame(root, width=400, height=400)
frame.pack()

panel = Label(frame, bg="white", width=400, height=400)
panel.place(x=0, y=0, relwidth=1, relheight=1)

scale_frame = Frame(root)
scale_frame.pack()

contrast_frame = Frame(scale_frame)
contrast_frame.pack()

contrast_var = IntVar()
smooth_var = DoubleVar(value=0.)

contrast_scale = Scale(contrast_frame, label="Contrast", variable=contrast_var, orient="horizontal",
                       length=255, from_=1, to=255, command=lambda value: update_image(contrast_var.get(), smooth_var.get()))
contrast_scale.set(128)
contrast_scale.pack(side="left")

smooth_frame = Frame(scale_frame)
smooth_frame.pack()

smooth_scale = Scale(smooth_frame, label="Smoothness", variable=smooth_var, resolution=0.05, orient="horizontal",
                     length=255, from_=0.0, to=10.0, command=lambda value: update_image(contrast_var.get(), smooth_var.get()))
smooth_scale.set(0)
smooth_scale.pack(side="left")

button_frame = Frame(root)
button_frame.pack()

open_button = Button(
    button_frame, text="Open", command=lambda: open_img(contrast_var.get(), smooth_var.get()))
open_button.pack(side="left", anchor="center")

save_button = Button(button_frame, text="Save", command=lambda: save(bw_image))
save_button.pack(side="left", anchor="center")

root.mainloop()
