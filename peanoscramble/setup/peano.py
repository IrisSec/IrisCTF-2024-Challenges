from PIL import Image

step = 10
angle = 1
x = 0
y = -1
inpx = 0
inpy = 0

width, height = 729, 729
inpimage = Image.open("flag.png")
image = Image.new("RGB", (width, height), "white")

def put_pixel():
    global inpimage, inpx, inpy, width, height
    d = inpimage.getpixel((inpx, inpy))
    image.putpixel((x, y), d)
    inpx += 1
    if inpx >= width:
        inpx = 0
        inpy += 1

# https://commons.wikimedia.org/wiki/File:Peano_curve_square_order.svg
def draw():
    global angle, x, y, image
    angle %= 4
    if angle == 0:
        x += 1
    elif angle == 1:
        y -= 1
    elif angle == 2:
        x -= 1
    elif angle == 3:
        y += 1
    
    put_pixel()

def fractal(depth, divided_angle):
    global angle
    if depth <= 0:
        return
    depth -= 1
    fractal(depth, divided_angle)
    draw()
    fractal(depth, -divided_angle)
    draw()
    fractal(depth, divided_angle)
    angle += divided_angle
    draw()
    angle += divided_angle
    fractal(depth, -divided_angle)
    draw()
    fractal(depth, divided_angle)
    draw()
    fractal(depth, -divided_angle)
    angle -= divided_angle
    draw()
    angle -= divided_angle
    fractal(depth, divided_angle)
    draw()
    fractal(depth, -divided_angle)
    draw()
    fractal(depth, divided_angle)

put_pixel()
fractal(6, 3)

image.save("chal.png")