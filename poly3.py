import pygame,math

import pygame

def draw_textured_rect(surf_arr, tex_arr, verts,rot):
    min_y = max(int(min(y for (x,y),_ in verts)),0)
    max_y = min(int(max(y for (x,y),_ in verts)),surf_arr.shape[0])

    edges = []
    for i in range(4):
        p1,p2 = verts[i],verts[(i+1)&3]
        if p1[0][1] == p2[0][1]: continue
        if p1[0][1] > p2[0][1]: p1,p2 = p2,p1
        edges.append((p1,p2))

    for y in range(min_y, max_y):
        # 2点を求める
        pts = []
        for ((x1,y1),(u1,v1)),((x2,y2),(u2,v2)) in edges:
            if y1 <= y < y2:
                t = (y - y1) / (y2 - y1)
                x = x1 + (x2 - x1) * t
                u = u1 + (u2 - u1) * t
                v = v1 + (v2 - v1) * t
                pts.append((x,u,v))
        if len(pts) != 2: continue
        (x1,u1,v1),(x2,u2,v2) = sorted(pts, key=lambda p:p[0])

        # スパン描画
        w = x2 - x1
        if w <= 0: continue
        du = (u2 - u1) / w; dv = (v2 - v1) / w
        for x in range(int(x1), min(int(x1)+int(w),surf_arr.shape[1])):
            if 0 <= x:
                surf_arr[x, y] = tex_arr[int(v1), int(u1)]
            u1 += du; v1 += dv

def fill_rect(arr,tex,x,y,w,h,u1,v1,u2,v2,rot=0):
    u2-=0.0001
    v2-=0.0001
    w = w/2
    h = h/2
    rot = rot * math.pi / 128
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
    vs = [(ps[0],(u1,v1)),(ps[1],(u2,v1)),(ps[2],(u2,v2)),(ps[3],(u1,v2))]
    draw_textured_rect(arr,tex,vs,rot)

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
    surface.fill((0,0,128))

    arr = pygame.surfarray.pixels3d(surface)
    fill_rect(arr,tarr,64,64,128,128,0,0,w,h,rot)
    del arr
    rot = (rot + 1) & 255
    screen.blit(pygame.transform.scale(surface,(512,448)),(0,0))
    clock.tick(60)
    pygame.display.flip()
del tarr
pygame.quit()

