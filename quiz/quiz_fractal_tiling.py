# Shadertoy "Fractal Tiling", reference ==> https://www.shadertoy.com/view/Ml2GWy#

import taichi as ti
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import handy_shader_functions as hsf #import the handy shader functions from the parent folder

ti.init(arch=ti.cpu)

res_x = 768
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))


@ti.kernel
def render(t: ti.f32):
    for i_, j_ in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        
        tile_size = 3

        offset = int(t*5) # make it move
        i = i_ + offset
        j = j_ + offset

        for k in range(6):
            ... # do something

        color = hsf.clamp(color, 0.0, 1.0)

        pixels[i_, j_] = color

gui = ti.GUI("Fractal Tiling", res=(res_x, res_y))

for i in range(1000000):
    render(i*0.05)
    gui.set_image(pixels)
    gui.show()