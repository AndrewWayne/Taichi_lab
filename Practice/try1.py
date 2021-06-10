import taichi as ti

ti.init(arch = ti.metal)
n = 320
pixels = ti.field(ti.f32, shape = (n, n))
iter = 0.0

@ti.func
def distance(x1, y1, x2, y2) -> ti.f32:
    xx = (x1 - x2)
    yy = (y1 - y2)
    return xx*xx + yy*yy

@ti.kernel
def paint(iter:ti.f32):
    #if iter == 1 :
    theta = iter
    sina = ti.sin(theta)
    cosa = ti.cos(theta)
    for i, j in pixels:
        pixels[i, j] = 1
        if distance(i, j, n/2 + 25 * sina, n/2 + 25 * cosa) < 625:
            pixels[i, j] = 1
        elif distance(i, j, n/2, n/2) < 2500 and sina * (j - n/2) - cosa * (i - n/2) < 0: # y < sin/cos x <==> y - sin/cos x < 0 <==> (cosy - sinx)*cos < 0
            pixels[i, j] = 0
        elif distance(i, j, n/2 - 25 * ti.sin(theta), n/2 - 25 * ti.cos(theta)) < 625:
            pixels[i,j] = 0
        if distance(i, j, n/2 + 25 * ti.sin(theta), n/2 + 25 * ti.cos(theta)) < 100:
            pixels[i, j] = 0
        if distance(i, j, n/2 - 25 * ti.sin(theta), n/2 - 25 * ti.cos(theta)) < 100:
            pixels[i, j] = 1
        if 2500 <= distance(i, j, n/2, n/2) < 2600:
            pixels[i,j] = 0
    #else :




gui = ti.GUI("Try1", res = (n, n))
speedg = gui.slider('Speed', 0.01, 10)
#for i in range(10000000):
while gui.running:
    iter += speedg.value
    paint(iter)
    gui.set_image(pixels)
    gui.show()
