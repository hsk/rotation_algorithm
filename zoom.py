import pygame,math
pygame.init()
screen = pygame.display.set_mode((256*3, 224*3))
surface = pygame.Surface((256, 224))
img = pygame.image.load("tex.png")

def draw_img(surface,img,rect1,rect2,rot):
    sub = img.subsurface(rect1)# 切り出し
    sub = pygame.transform.scale(sub, (rect2[2], rect2[3])) # リサイズ
    sub = pygame.transform.rotate(sub, rot*180/math.pi)  # 回転
    dst_rect = sub.get_rect(center=(rect2[0]+rect2[2]//2, rect2[1]+rect2[3]//2))
    surface.blit(sub, dst_rect)# rect2へblit

running = True
rot = 0
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    zoom = math.cos(rot)*4 + 4*2
    rot += 0.01
    surface.fill((0,0,0))
    rect1 = (0, 0, 16, 16)   # 画像1から切り取る範囲
    rect2 = (128-8*zoom, 112-8*zoom, 16*zoom+0.5, 16*zoom+0.5)   # 転送先の位置とサイズ
    draw_img(surface,img,rect1,rect2,rot)

    # 2倍に拡大して表示
    scaled = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
    screen.blit(scaled, (0,0))

    pygame.display.flip()

pygame.quit()