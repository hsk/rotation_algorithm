import pygame, math

pygame.init()
w, h = 256, 192
cx, cy = w // 2, h // 2 # 画面中央
screen = pygame.display.set_mode((w*3, h*3))
suf = pygame.Surface((w,h))
#tex = pygame.image.load("rot.png").convert()
tex = pygame.image.load("tex4.png").convert()
tcx = tex.get_width()//2
tcy = tex.get_height()//2
tmax = int(max(tcx+tcx//2,tcy+tcy//2))
clock = pygame.time.Clock()
def main():
    running = True
    r = 0; cnt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        suf.fill((0,0,64))
        cos =  math.cos(r)
        sin =  math.sin(r)
        if True: # 上方向
            sx = tcx; sy = tcy
            for y in range(cy-1,0,-1):
                sx +=  cos*0+sin*-1
                sy += -sin*0+cos*-1
                flg = False
                if True: # 右上方向
                    ox = sx; oy = sy
                    for x in range(cx,cx+tmax):
                        if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                            col = tex.get_at((int(ox) & 255, int(oy) & 255))
                            suf.set_at((x, y), col)
                            flg = True
                        elif flg: break
                        else: suf.set_at((x, y), (64,0,64))
                        ox +=  cos * 1 + sin * 0
                        oy += -sin * 1 + cos * 0
                if True: # 左上方向
                    ox = sx; oy = sy
                    for x in range(cx-1,cx-tmax,-1):
                        ox +=  cos * -1 + sin * 0
                        oy += -sin * -1 + cos * 0
                        if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                            col = tex.get_at((int(ox) & 255, int(oy) & 255))
                            suf.set_at((x, y), col)
                            flg = True
                        elif flg: break
                        else: suf.set_at((x, y), (64,64,0))
                if not flg: break

        if True: # 下方向
            sx = tcx; sy = tcy
            for y in range(cy,h):
                flg = False
                if True: # 右下方向
                    ox = sx; oy = sy
                    for x in range(cx,cx+tmax):
                        if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                            col = tex.get_at((int(ox) & 255, int(oy) & 255))
                            suf.set_at((x, y), col)
                            flg = True
                        elif flg: break
                        else: suf.set_at((x, y), (64,0,0))
                        ox +=  cos * 1 + sin * 0
                        oy += -sin * 1 + cos * 0
                if True: # 左下方向
                    ox = sx; oy = sy
                    for x in range(cx-1,cx-tmax,-1):
                        ox +=  cos * -1 + sin * 0
                        oy += -sin * -1 + cos * 0
                        if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                            col = tex.get_at((int(ox) & 255, int(oy) & 255))
                            suf.set_at((x, y), col)
                            flg = True
                        elif flg: break
                        else: suf.set_at((x, y), (0,64,0))
                if not flg: break
                sx +=  cos*0+sin*1
                sy += -sin*0+cos*1
        r += 0.05

        clock.tick(60)
        screen.blit(pygame.transform.scale(suf,(w*3,h*3)),(0,0))
        pygame.display.flip()
        pygame.image.save(screen, f"m/{cnt:03d}.png")
        cnt += 1

main()
