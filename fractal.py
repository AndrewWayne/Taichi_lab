import taichi as ti

ti.init(arch = ti.gpu)
n = 1200
pixels = ti.field(ti.f32, shape=(2400, 1200))

@ti.func
def complex_power(z, power:ti.i32):
    r = ti.sqrt(z[0]**2 + z[1]**2)
    theta = ti.atan2(z[1], z[0])
    return ti.Vector([r**power * ti.cos(power*theta), r**power * ti.sin(power*theta)])

@ti.kernel
def paint(t: ti.f32, power: ti.i32, re: ti.f32, im: ti.f32):
    re = re
    im = im
    for i, j in pixels:  # Parallized over all pixels
        freq = 1.0 / power
        #c = ti.Vector([0.7885 * ti.cos(freq*t), 0.7885 * ti.sin(freq*t)])
        c = ti.Vector([0.7885 * ti.cos(freq*t)*re, 0.7885 * ti.sin(freq*t)*im])
        z = ti.Vector([i / n - 1, j / n - 0.5]) * 2

        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_power(z, power) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02

power = eval(input("Power of z -> "))
gui = ti.GUI("Julia Set", res=(2400, 1200))
for i in range(10000000):
    re, im = gui.get_cursor_pos()
    paint(i * 0.03, power, re, im)
    #paint(i * 0.03, power)
    gui.set_image(pixels)
    gui.show()
