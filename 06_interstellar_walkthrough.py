# An example contributed by Andrew Sun (https://github.com/victoriacity)

import math
import taichi as ti


ti.init(arch=ti.cuda)
res = (800, 600)
grid_spacing = 120
far = 3600 # also use pixel coordinates in z axis
near = 600
fov = 60 # horizontal field of view
radius = 2.5 # particle radius in pixels
shutter = 0.1
tanfov = math.tan(fov * math.pi / 180)
n_grids = (
    res[0] // grid_spacing,
    res[1] // grid_spacing,
    (far - near) // grid_spacing,
)
n_particles = int(n_grids[0] * n_grids[1] * n_grids[2])


pos = ti.Vector.field(3, dtype=float, shape=n_particles)
col = ti.Vector.field(3, dtype=float, shape=n_particles)
speed = ti.field(dtype=float, shape=()) # pixel per second
mainimg = ti.Vector.field(3, dtype=float, shape=res)


@ti.func
def rand3():
    return ti.Vector([ti.random(), ti.random(), ti.random()])


@ti.func
def spawn(grid_idx, i):
    pos[i] = (grid_idx + rand3()) \
            * grid_spacing
    pos[i][2] += float(near)
    col[i] = ti.Vector([1, 2, 3]) + rand3() # ad-hoc linear color space


@ti.kernel
def initialize():
    for i in pos:
        # calculate grid index
        grid_x = i // (n_grids[1] * n_grids[2])
        grid_y = (i % (n_grids[1] * n_grids[2])) // n_grids[2]
        grid_z = i % n_grids[2]
        spawn(ti.Vector([grid_x, grid_y, grid_z]), i)


@ti.func
def project(v):
    # assume camera is located at center of view space
    center = ti.Vector(res) / 2
    w = tanfov * v.z
    rel_pos = (ti.Vector([v.x, v.y]) - center) / w
    return rel_pos * res[0] + center


@ti.func
def depth_fade(v):
    fac = (v.z - near) / (far - near)
    return 1 - fac ** 0.5


@ti.func
def radius_fade(r_sqr, r_view):
    fac = r_sqr / (r_view ** 2)
    return 1 - fac ** 0.2


@ti.func
def draw_particle(v, color, radius, opacity):
    v_view = project(v)
    r_view = project(v + ti.Vector([0, radius, 0])).y - v_view.y
    X_low, X_high = int(v_view.x - r_view) - 1, int(v_view.x + r_view) + 1
    Y_low, Y_high = int(v_view.y - r_view) - 1, int(v_view.y + r_view) + 1
    if (X_low < res[0] or X_high >= 0 or Y_low < res[1] or Y_high >= 0):
        for I in ti.grouped(ti.ndrange((X_low, X_high), (Y_low, Y_high))):
            if 0 <= I.x < res[0] and 0 <= I.y < res[1]:
                r_sqr = ((I - v_view) ** 2).sum()
                if r_sqr <= r_view ** 2:
                    mainimg[I] += opacity * color \
                       * depth_fade(v) \
                       * radius_fade(r_sqr, r_view) \


@ti.func
def draw(v, color, radius):
    pixel_exposed = int(ti.ceil(shutter * speed[None]))
    norm = pixel_exposed * (pixel_exposed + 1) / 2
    for t in range(pixel_exposed):
        v_traj = v - ti.Vector([0, 0, t])
        opacity = (t + 1) / norm * 0.95 + 0.05
        draw_particle(v_traj, color, radius, opacity)


@ti.func
def respawn_far(i):
    grid_x = i // (n_grids[1] * n_grids[2])
    grid_y = (i % (n_grids[1] * n_grids[2])) // n_grids[2]
    grid_z = n_grids[2] - 1
    spawn(ti.Vector([grid_x, grid_y, grid_z]), i)


@ti.kernel
def step():
    for i in pos:
        draw(pos[i], col[i], radius)
        pos[i][2] = pos[i][2] - speed[None] / fps
        if pos[i][2] < near:
            respawn_far(i)


initialize()
speed[None] = 500
gui = ti.GUI('Warp', res, fast_gui=True)
time = 0
fps = 60
while gui.running:
    # uncomment the line below to change speed with time
    speed[None] = 20 + (1 - math.cos(time * math.pi / 4.0)) * 500
    mainimg.fill(0)
    step()
    gui.set_image(mainimg)
    time += 1.0 / fps
    gui.show()