# Shadertoy "Fractal Tiling", reference ==> https://www.shadertoy.com/view/Ml2GWy#

import taichi as ti

ti.init(arch=ti.cpu)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.func
def clamp(v, v_min, v_max):
    return ti.max(ti.min(v, v_max), v_min)

@ti.func
def fract(x):
    return x - ti.floor(x)

@ti.func
def smoothstep(edge1, edge2, v):
    assert(edge1 != edge2)
    t = (v-edge1) / float(edge2-edge1)
    t = clamp(t, 0.0, 1.0)

    return (3-2 * t) * t**2

@ti.kernel
def render(t: ti.f32):
    for i_, j_ in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        
        tile_size = 96

        offset = int(t*5) # make it move
        i = i_ + offset
        j = j_ + offset

        layers = 6
        for k in range(layers):
            pos = ti.Vector([i % tile_size, j % tile_size]) # keeps the pos in [0, tile_size - 1]
            tile_id = ti.Vector([i // tile_size, j//tile_size]) # save the tile ids as the random number seeds
            uv = pos / float(tile_size) # uv coordinates in [0.0, 1.0)

            time_dependent_rand = fract(ti.sin(tile_id[0]*7 + tile_id[1]*31 + 0.0005 * t) * 128)
            square_opacity = smoothstep(0.2, 0.6, time_dependent_rand) # add some randomness to the opacity
            square_intensity = time_dependent_rand * ti.sqrt(16.0 * uv[0]*uv[1]*(1.0-uv[0])*(1.0-uv[1])) # color intensity in [0.0, 1.0], brighter in the middle and dimmer in the corners
            square_color = ti.Vector([1, time_dependent_rand * 0.8, time_dependent_rand * 0.8]) #control the color
            # square_color = fract(ti.Vector([0.1, 0.2, 0.3]) + time_dependent_rand) #control the color

            layer_color = square_color * square_intensity * square_opacity
            layer_color *= 0.5 ** k

            color += layer_color
            tile_size = tile_size // 2

        color = clamp(color, 0.0, 1.0)

        pixels[i_, j_] = color

gui = ti.GUI("Fractal Tiling", res=(res_x, res_y))

for i in range(1000000):
    render(i*0.05)
    gui.set_image(pixels)
    gui.show()