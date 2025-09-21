import pygame,math

def draw_textured_triangle(arr, tex, verts):
    # yでソート
    verts = [((v[0][0],int(v[0][1])),v[1]) for v in verts]
    verts = sorted(verts, key=lambda v: v[0][1])
    (x0,y0),(u0,v0) = verts[0]
    (x1,y1),(u1,v1) = verts[1]
    (x2,y2),(u2,v2) = verts[2]

    def edge_interp(xa,ya,ua,va, xb,yb,ub,vb):
        if yb==ya: return []
        dy = yb-ya
        dx = (xb-xa)/dy
        du = (ub-ua)/dy
        dv = (vb-va)/dy
        for y in range(ya,yb):
            yield xa, ua, va
            xa += dx; ua += du; va += dv

    # 左右辺を生成
    left  = list(edge_interp(x0,y0,u0,v0, x2,y2,u2,v2))
    right = list(edge_interp(x0,y0,u0,v0, x1,y1,u1,v1)) + \
            list(edge_interp(x1,y1,u1,v1, x2,y2,u2,v2))
    if left[len(left)//2][0]>right[len(right)//2][0]:left,right=right,left
    for y in range(min(len(left),len(right))):
        xl,ul,vl = left[y]
        xr,ur,vr = right[y]
        w = xr-xl if xr-xl!=0 else 1
        du = (ur-ul)/w; dv = (vr-vl)/w
        y += y0
        for x in range(int(xl),int(xr)):
            arr[x,y] = tex[int(ul),int(vl)][:3]
            ul+=du; vl+=dv

def fill_rect(arr,tex,x,y,w,h,tx,ty,tw,th,rot=0):
    tw += tx-0.00001
    th += ty-0.00001
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
    ps = [((-wcos - hsin + x), ( wsin - hcos + y)),
            (( wcos - hsin + x), (-wsin - hcos + y)),
            (( wcos + hsin + x), (-wsin + hcos + y)),
            ((-wcos + hsin + x), ( wsin + hcos + y))]
    vs = [(ps[0],(tx,ty)),(ps[1],(tw,ty)),(ps[2],(tw,th)),(ps[3],(tx,th))]
    verts = [vs[0], vs[1], vs[2]]
    #fill_poly(arr,tex,verts)
    draw_textured_triangle(arr,tex,verts)
    verts2 = [vs[2], vs[3],vs[0]]
    #fill_poly(arr,tex,verts2)
    draw_textured_triangle(arr,tex,verts2)

pygame.init()
screen = pygame.display.set_mode((512,448))
surface = pygame.Surface((256,224))
tex = pygame.image.load("tex.png").convert()
w,h = tex.get_size()

rot = 0
running = True
tarr = pygame.surfarray.pixels3d(tex)
clock = pygame.time.Clock()
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
    surface.fill((0,0,0))

    arr = pygame.surfarray.pixels3d(surface)
    fill_rect(arr,tarr,64,64,128,128,0,0,w//2,h//2,rot)
    del arr
    rot += 0.05
    screen.blit(pygame.transform.scale(surface,(512,448)),(0,0))
    clock.tick(10)
    pygame.display.flip()
del tarr
pygame.quit()

