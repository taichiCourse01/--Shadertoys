# reference ==> 

import taichi as ti
import handy_shader_functions as hsf

ti.init(arch = ti.cpu)

res_x = 512
res_y = 512
scatter = 1
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
    center = ti.Vector([res_x//scatter//2, res_y//scatter//2])
    r1 = 100.0 / scatter

    for i,j in pixels:     
        color = ti.Vector([0.0, 0.0, 0.0]) # init your canvas to white
        pos = ti.Vector([i//scatter, j//scatter])
        r = (pos - center).norm() 

        # # discrete circle
        # if r <= r1:
        #     color = ti.Vector([1.0, 1.0, 1.0])

        # # smooth circle
        # color = ti.Vector([1.0, 1.0, 1.0]) * (1.0-r/r1)

        # # smooth circle 2
        # color = ti.Vector([1.0, 1.0, 1.0]) * hsf.smoothstep(1.0, 0.8, r/r1)

        c = circle(pos, center, r1, 0.1)
        mask = c

        c2 = square(pos, center, 30.0/scatter, 0.1)
        mask -= c2

        color = ti.Vector([1.0, 1.0, 0.0]) * mask
        pixels[i, j] = color

gui = ti.GUI("Solid Circle", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()