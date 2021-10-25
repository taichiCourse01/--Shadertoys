# reference ==> https://www.shadertoy.com/view/MdlXz8

import taichi as ti
import handy_shader_functions as hsf

ti.init(arch = ti.cuda)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

PI = 3.1415926
TAU = 2*PI

@ti.kernel
def render(time:ti.f32):
    # draw something on your canvas
    for i,j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0]) # init your canvas to black

        uv = ti.Vector([float(i)/res_x, float(j)/res_y])

        p = hsf.mod(uv * TAU, TAU) - 250.0       
        
        p2 = p
        c = 1.0
        inten = 0.005

        max_iter = 5
        for k in range(max_iter):
            t = time * (1.0 - (3.5 / float(k+1)))
            p2 = p + ti.Vector([ti.cos(t-p2.x) + ti.sin(t+p2.y), ti.sin(t-p2.y)+ti.cos(t+p2.x)])
            c += 1.0/(ti.Vector([p.x / (ti.sin(p2.x+t)/inten), p.y / (ti.cos(p2.y + t) / inten)])).norm()
        
        c /= float(max_iter)
        c = 1.17 - c**1.4 # reverse
        c = c ** 8 # making it sharp
        color = ti.Vector([1.0, 1.0, 1.0]) * c

        color += hsf.clamp(ti.Vector([0.0, 0.35, 0.5]), 0.0, 1.0) # turning blue

        pixels[i,j] = color

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()