import taichi as ti

@ti.func
def smoothstep(v_min, v_max, v):
    t = 0.0
    if v_min >= v_max:
        if v < v_min: t =0
        else: t = 1
    else:
        if v < v_min: v = v_min
        elif v > v_max: v = v_max
        t = (v-v_min) / float(v_max-v_min)

    return -2 * t**3 + 3 * t ** 2

@ti.func
def linearstep(v_min, v_max, v):
    t = 0.0
    if v_min >= v_max:
        if v < v_min: t =0
        else: t = 1
    else:
        if v < v_min: v = v_min
        elif v > v_max: v = v_max
        t = (v-v_min) / float(v_max-v_min)

    return t

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