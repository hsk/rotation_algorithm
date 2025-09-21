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
    cos = math.cos(rot) # 回転角のcos
    sin = math.sin(rot) # 回転角のsin

    x = cx; y = cy     # x,yは描画先の画面座標
    tx = tcx; ty = tcy # tx,tyはテクスチャ座標
    # 上方向（yを減少させる）に進むので、テクスチャ座標の増分も反転させる
    dtx =  cos*0+sin*-1
    dty = -sin*0+cos*-1
    dx = dtx
    # pyを減少方向にスキャン
    while 0 < y:
        if 0 <= y < surf_arr.shape[1]:
            fill(surf_arr,tex_arr,tw,th,-1,-cos,-sin,int(x),y,tx,ty)
            fill(surf_arr,tex_arr,tw,th,1,cos,sin,int(x),y,tx,ty,False)
        y-=1; tx -= dtx; ty -= dty; x -= dx

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
