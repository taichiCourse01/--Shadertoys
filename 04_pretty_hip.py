# reference ==> https://www.shadertoy.com/view/XsBfRW

import taichi as ti
import handy_shader_functions as hsf

ti.init(arch = ti.cuda)

res_x = 512
res_y = 256
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t:ti.f32):
    # draw something on your canvas
    for i,j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0]) # init your canvas to black
        aspect = float(res_y) / float(res_x)
        uv = ti.Vector([float(i) / res_x, float(j) / res_x])

        shift = ti.Vector([0.5, 0.5*aspect])
        uv -= shift
        angle = 45.0 / 180.0 * 3.1415926 # 45 degrees in radius
        R = ti.Matrix([[ti.cos(angle), ti.sin(angle)],[-ti.sin(angle), ti.cos(angle)]])
        uv = R@uv
        uv += shift
        uv[1] += 0.5*(1-aspect)
        
        pos = 10*uv
        rep = hsf.fract(pos)
        dist = 2.0*ti.min(ti.min(rep.x, 1.0-rep.x), ti.min(rep.y, 1.0-rep.y))
        squareDist = (hsf.floor(pos) - 4.5).norm()

        edge = ti.sin(t - squareDist*0.5) + 0.5
        edge = 2.0*hsf.fract(edge*0.5)
        value = hsf.fract(dist*2.0)

        pixels[i,j] = color
        value = hsf.lerp(value, 1-value, hsf.step(1.0, edge))
        edge = ti.pow(ti.abs(1.0-edge), 2.0)
        
        value = hsf.smoothstep(edge-0.05, edge, 0.95*value)

        value += squareDist * 0.1

        color[0] = hsf.lerp(1.0, 0.5, value)
        color[1] = hsf.lerp(1.0, 0.75, value)
        color[2] = 1.0

        pixels[i,j] = color

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()