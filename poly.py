import pygame,math


def fill_poly(arr,verts):
    def barycentric_int(p, a, b, c):
        # 分母
        det = (b[1]-c[1])*(a[0]-c[0]) + (c[0]-b[0])*(a[1]-c[1])
        # 各分子
        num1 = ( (b[1]-c[1])*(p[0]-c[0]) + (c[0]-b[0])*(p[1]-c[1]) )
        num2 = ( (c[1]-a[1])*(p[0]-c[0]) + (a[0]-c[0])*(p[1]-c[1]) )
        num3 = det - num1 - num2
        return num1, num2, num3, det
    # 三角形の外接矩形
    xs = [v[0][0] for v in verts]; ys=[v[0][1] for v in verts]
    minx,maxx = int(min(xs)), int(max(xs))
    miny,maxy = int(min(ys)), int(max(ys))

    for y in range(miny, maxy):
        for x in range(minx, maxx):
            # 使用例
            num1, num2, num3, det = barycentric_int((x,y), *[v[0] for v in verts])
            if num1>=0 and num2>=0 and num3>=0:
                u = (num1*verts[0][1][0] + num2*verts[1][1][0] + num3*verts[2][1][0]) / det
                v = (num1*verts[0][1][1] + num2*verts[1][1][1] + num3*verts[2][1][1]) / det
                color = tex.get_at((int(u),int(v)))
                arr[x, y] = (color.r, color.g, color.b)
def fill_rect(arr,x,y,w,h,tx,ty,tw,th,rot=0):
    tw += tx
    th += ty
    if rot != 0:
        w = w/2
        h = h/2
        cos = math.cos(rot)
        sin = math.sin(rot)
        x += w
        y += h
        wcos = w * cos
        wsin = w * sin
        hcos = h * cos
        hsin = h * sin
        ps = [(-wcos - hsin + x,  wsin - hcos + y),
              ( wcos - hsin + x, -wsin - hcos + y),
              ( wcos + hsin + x, -wsin + hcos + y),
              (-wcos + hsin + x,  wsin + hcos + y)]
    else:
        w += x
        h += y
        ps = [(x,y),(w,y),(w,h),(x,h)]
    vs = [(ps[0],(tx,ty)),(ps[1],(tw,ty)),(ps[2],(tw,th)),(ps[3],(tx,th))]
    verts = [vs[0], vs[1], vs[2]]
    fill_poly(arr,verts)
    verts2 = [vs[2], vs[3],vs[0]]
    fill_poly(arr,verts2)

pygame.init()
screen = pygame.display.set_mode((512,448))
surface = pygame.Surface((256,224))
tex = pygame.image.load("tex.png").convert()
w,h = tex.get_size()

rot = 0
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
    surface.fill((0,0,0))

    arr = pygame.surfarray.pixels3d(surface)
    fill_rect(arr,64,64,128,128,0,0,w//2,h//2,rot)
    del arr
    rot += 0.05
    screen.blit(pygame.transform.scale(surface,(512,448)),(0,0))
    pygame.display.flip()
pygame.quit()
