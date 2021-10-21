# reference ==> 

import taichi as ti

ti.init(arch = ti.cpu)

res_x = 512
res_y = 512
scatter = 1
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t:ti.f32):
    r = 100 // scatter
    center = ti.Vector([res_x//scatter//2, res_y//scatter//2])
    for i,j in pixels:
        pixels[i, j] = ti.Vector([1, 1, 1])
        
        pos = ti.Vector([i//scatter, j//scatter])
        if (pos-center).norm() < r:
            pixels[i, j] = ti.Vector([0, 0, 1]) # blue


gui = ti.GUI("Solid Circle", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()