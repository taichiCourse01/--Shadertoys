# 太极图形课S1-Procedural Animations示例程序-Shadertoys

## 背景简介
本文实现了一些Procedural Animation的示例程序。
其中不少是借鉴的Shadertoy.com上的对应例子写的。

## 课堂Quiz
请填写./quiz/quiz_fractal_tiling.py以达到(类似的)如下效果：
### Fractal tiling (# reference ==> https://www.shadertoy.com/view/Ml2GWy#)
![tiling demo](./data/fractal_tiling.gif)

## 其他效果展示
### Circles tiling
![circles demo](./data/circles.gif)

### Fancy galaxy (reference ==> https://www.shadertoy.com/view/MdXSzS)
![galaxy demo](./data/galaxy.gif)

### Pretty hip (# reference ==> https://www.shadertoy.com/view/XsBfRW)
![galaxy demo](./data/pretty_hip.gif)

### Water caustic (# reference ==> https://www.shadertoy.com/view/MdlXz8)
![caustic demo](./data/caustic.gif)

### Interstellar (by Andrew Sun (https://github.com/victoriacity))
![interstellar demo](./data/interstellar.gif)

### The 3D slides of a 4D Julia-set (by Dunfan Lu (https://github.com/AmesingFlank))
![interstellar demo](./data/julia_4d.gif)


## 运行环境

```
[Taichi] version 0.8.3, llvm 10.0.0, commit 021af5d2, win, python 3.8.10
```

## 运行方式
确保handy_shader_functions.py可以访问的情况下，可以直接运行：`python3 [*].py`

其中`07_julia_4d.py`需要`GGUI`的支持
