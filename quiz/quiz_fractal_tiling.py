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
    for i, j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        
        tile_size = 3

        offset = int(t*5) # make it move
        row = i + offset
        col = j + offset

        # for k in range(6):

        #     pos = ti.Vector([hsf.mod(row, tile_size), hsf.mod(col, tile_size)]) # keeps the pos in [0, tile_size - 1]
        #     tile_id = ti.Vector([row // tile_size, col//tile_size]) # save the tile ids as the random number seeds
        #     uv = pos / float(tile_size) # uv coordinates in [0.0, 1.0])

        #     time_dependent_rand = ti.sin(tile_id[0]*0.7 + tile_id[1]*3.1 + 0.01 * t)
        #     square_color = hsf.fract(ti.Vector([0.1, 0.2, 0.3]) + time_dependent_rand) # add some randomness to the color
        #     square_opacity = hsf.smoothstep(0.45, 0.55, hsf.fract(time_dependent_rand)) # add some randomness to the opacity

        #     square_intensity = ti.sqrt(16.0 * uv[0]*uv[1]*(1.0-uv[0])*(1.0-uv[1])) # color intensity in [0.0, 1.0], brighter in the middle and dimmer in the corners

        #     color += 2 * square_color * square_intensity * square_opacity # multiply by two because we are going to reduce it by half at the end

        #     tile_size *= 2.0
        #     color /= 2.0

        color = hsf.clamp(color, 0.0, 1.0)

        pixels[i, j] = color

gui = ti.GUI("Fractal Tiling", res=(res_x, res_y))

for i in range(1000000):
    render(i*0.05)
    gui.set_image(pixels)
    gui.show()