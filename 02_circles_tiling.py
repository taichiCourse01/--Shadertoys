# reference ==> 

import taichi as ti
import handy_shader_functions as hsf

ti.init(arch = ti.cuda)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ ti.func
def circle(pos, center, radius, blur):
    r = (pos - center).norm()
    t = 0.0
    if blur > 1.0: blur = 1.0
    if blur <= 0.0: 
        t = 1.0-hsf.step(1.0, r/radius)
    else:
        t = hsf.smoothstep(1.0, 1.0-blur, r/radius)
    return t

@ti.func
def square(pos, center, radius, blur):
    diff = ti.abs(pos-center)
    r = ti.max(diff[0], diff[1])
    t = 0.0
    if blur > 1.0: blur = 1.0
    if blur <= 0.0: 
        t = 1.0-hsf.step(1.0, r/radius)
    else:
        t = hsf.smoothstep(1.0, 1.0-blur, r/radius)
    return t

@ti.kernel
def render(t:ti.f32):
    # draw something on your canvas
    for i,j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0]) # init your canvas to black

        tile_size = 16
        for k in range(3):
            
            center = ti.Vector([tile_size//2, tile_size//2])
            radius = tile_size//2

            pos = ti.Vector([hsf.mod(i, tile_size), hsf.mod(j, tile_size)]) # scale i, j to [0, tile_size-1]
            
            blur =hsf.fract(ti.sin(float(0.1*t+i//tile_size*5+j//tile_size*3)))
            c = circle(pos, center, radius, blur)
            
            r = 0.5*ti.sin(float(0.001*t+i//tile_size)) + 0.5
            g = 0.5*ti.sin(float(0.001*t+j//tile_size) + 2) + 0.5
            b = 0.5*ti.sin(float(0.001*t+i//tile_size) + 4) + 0.5

            color += ti.Vector([r, g, b])*c
            
            color /= 2
            tile_size *= 2

        pixels[i,j] = color

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()