import pygame,math

import pygame
def fill(surf_arr,tex_arr,tw,th,dx,dtx,dty,x,y,tx,ty,c=True):
    sw = surf_arr.shape[0]
    if c: x+=dx; tx += dtx; ty += dty
    while 0 <= tx < tw and 0 <= ty < th:
        if 0 <= x < sw:
            surf_arr[x, y] = tex_arr[int(tx),int(ty)]
        x+=dx; tx += dtx; ty += dty

def fill_rect(surf_arr,tex_arr,cx,cy,rot=0):
    tw = tex_arr.shape[0]; th = tex_arr.shape[1] # 幅、高さ
    tcx = tw/2; tcy = th/2 # テクスチャ中心
    cos = math.cos(rot) # 45度の方向
    sin = math.sin(rot) # 45度の方向
    ps0 = [( tcx,  tcy), (-tcx, -tcy), ( tcx, -tcy), (-tcx,  tcy)]
    cs = [(0,255,0),(0,255,0),(255,0,0),(255,0,0)]
    ps = [((cos*p[0]+sin*p[1]),(-sin*p[0]+cos*p[1])) for p in ps0]
    tcx0 = tcx; tcy0 = tcy
    for i,p in enumerate(ps):
        #surf_arr[int(cx+p[0]), int(cy+p[1])] = cs[i] # 角の描画
        if math.fabs(ps[0][1]) < math.fabs(ps[2][1]):
            if i < 2: continue
        else:
            if i >= 2: continue
        print(f"{p[1]} ",end="")
        x = cx; dx = p[0]/p[1]
        y = cy
        tx = tcx; dtx = ps0[i][0]/p[1]
        ty = tcy; dty = ps0[i][1]/p[1]
        if (p[1]<0):
            while max(0,cy+p[1]) < y:
                if 0 <= y < surf_arr.shape[1]:
                    fill(surf_arr,tex_arr,tw,th,-1,-cos,-sin,int(x),y,tx,ty)
                    fill(surf_arr,tex_arr,tw,th,1,cos,sin,int(x),y,tx,ty,False)
                y-=1; x -= dx; tx -= dtx; ty -= dty
        else:
            while y < min(surf_arr.shape[1]-1,cy+p[1]-1):
                y+=1; x += dx; tx += dtx; ty += dty
                if 0 <= y < surf_arr.shape[1]:
                    fill(surf_arr,tex_arr,tw,th,-1,-cos,-sin,int(x),y,tx,ty)
                    fill(surf_arr,tex_arr,tw,th,1,cos,sin,int(x),y,tx,ty,False)
    print("")
pygame.init()
screen = pygame.display.set_mode((512,448))
surface = pygame.Surface((256,224))
tex = pygame.image.load("tex4.png").convert()
rot = 0
running = True
tarr = pygame.surfarray.pixels3d(tex)
clock = pygame.time.Clock()
x = 0; y = 0
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  x -= 1
    if keys[pygame.K_RIGHT]: x += 1
    if keys[pygame.K_UP]:    y -= 1
    if keys[pygame.K_DOWN]:  y += 1

    surface.fill((0,0,128))

    arr = pygame.surfarray.pixels3d(surface)
    fill_rect(arr,tarr,128+64,112-64,rot)
    #fill_rect(arr,tarr,128-64,112+64,rot*2)
    #fill_rect(arr,tarr,-1,112+64,rot*2)
    #fill_rect(arr,tarr,x,y,rot*2)
    del arr
    rot += 0.02
    screen.blit(pygame.transform.scale(surface,(512,448)),(0,0))
    clock.tick(60)
    pygame.display.flip()
del tarr
pygame.quit()
