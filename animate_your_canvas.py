# reference ==> 

import taichi as ti

ti.init(arch = ti.cpu)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t:ti.f32):
    # draw something on your canvas
    for i,j in pixels:
        r = 0.5 * ti.sin(t + float(i) / res_x) + 0.5
        g = 0.5 * ti.sin(t + float(j) / res_y + 2) + 0.5
        b = 0.5 * ti.sin(t + float(i) / res_x + 4) + 0.5
        color = ti.Vector([r, g, b])
        pixels[i, j] = color

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()