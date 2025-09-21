import pygame, math

pygame.init()
w, h = 256, 192
cx, cy = w // 2, h // 2 # 画面中央
suf = pygame.display.set_mode((w, h))
tex = pygame.image.load("rot.png").convert()

def main():
    running = True
    r = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        cos =  math.cos(r)
        sin =  math.sin(r)
        sx =  cos * -cx + sin * -cy + cx
        sy = -sin * -cx + cos * -cy + cy
        for y in range(h):
            ox = sx; oy = sy
            for x in range(w):
                col = tex.get_at((int(ox) & 255, int(oy) & 255))
                suf.set_at((x, y), col)
                ox +=  cos * 1 + sin * 0
                oy += -sin * 1 + cos * 0
            sx +=  cos*0+sin*1
            sy += -sin*0+cos*1
        r += 0.01

        pygame.display.flip()

main()
