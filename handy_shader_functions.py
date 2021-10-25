import taichi as ti

@ti.func
def swap(v1, v2):
    return (v2, v1)

@ti.func
def clamp(v, v_min, v_max):
    if v < v_min: v = v_min
    if v > v_max: v = v_max
    return v

@ti.func
def smoothstep(v1, v2, v):
    assert(v1 != v2)
    t = (v-v1) / float(v2-v1)
    t = clamp(t, 0.0, 1.0)

    return (3-2 * t) * t**2

@ti.func
def step(edge, v):
    ret = 0.0
    if (v < edge): ret = 0.0
    else: ret = 1.0
    return ret

@ti.func
def lerp(x, y, a):
    return x * (1-a) + y * a

@ti.func
def clamp3(vec, v_min, v_max):
    for i in ti.static(range(3)):
        if vec[i] < v_min: vec[i] = v_min
        if vec[i] > v_max: vec[i] = v_max
    return vec

@ti.func
def floor(vec):
    return ti.floor(vec)

@ti.func
def fract(vec):
    return vec - ti.floor(vec)

@ti.func
def mod(x, y):
    return x - y * ti.floor(x/y)