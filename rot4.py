import pygame, math

pygame.init()
w, h = 256, 192
cx, cy = w // 2, h // 2 # 画面中央
screen = pygame.display.set_mode((w*3, h*3))
suf = pygame.Surface((w,h))
#tex = pygame.image.load("rot.png").convert()
tex = pygame.image.load("tex4.png").convert()
clock = pygame.time.Clock()
def main():
    running = True
    r = 0; cnt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        suf.fill((0,0,64))
        cos = math.cos(r)
        sin = math.sin(r)
        draw_rotated_texture(suf, tex, cx, cy, w, h, cos, sin)
        r += 0.005

        clock.tick(60)
        screen.blit(pygame.transform.scale(suf,(w*3,h*3)),(0,0))
        pygame.display.flip()
        pygame.image.save(screen, f"m/{cnt:03d}.png")
        cnt += 1


def draw_rotated_texture(suf, tex, cx, cy, w, h, cos, sin):
    tcx = tex.get_width()//2
    tcy = tex.get_height()//2
    tmax = int(max(tcx+tcx//2,tcy+tcy//2))
    bkcx = cx
    # 下方向のループ：画面中央から下に向かって走査し、座標は足し算と引き算で計算
    sx = tcx; sy = tcy
    for y in range(cy,h):
        # 右下方向のループ：右下方向に走査し、座標計算は足し算・引き算のみ
        ox = sx; oy = sy
        right = None; left = None
        x = cx
        while True:
            if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                col = tex.get_at((int(ox) & 255, int(oy) & 255))
                suf.set_at((x, y), col)
                right = x
            else: break
            ox += cos; oy += -sin; x += 1
        # 左下方向のループ：左下方向に走査し、座標計算は足し算・引き算のみ
        ox = sx; oy = sy; x = cx - 1
        while True:
            ox -= cos; oy += sin
            if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                col = tex.get_at((int(ox) & 255, int(oy) & 255))
                suf.set_at((x, y), col)
                left = x; x -= 1
            else: break
        # 次のY座標の開始位置を求める
        find = False
        sx += sin; sy += cos
        if 0 <= sx < tex.get_width() and 0 <= sy < tex.get_height():
            find = True
        # 1. 中心から右へ検索
        elif right != None:
            ox = sx; oy = sy; x = cx
            while x <= right:
                x += 1; ox += cos; oy -= sin    # 回転座標を対応してずらす
                if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                    find = True
                    cx = x; sx = ox; sy = oy
                    break
        # 2. 左へ検索
        if not find and left != None:
            ox = sx; oy = sy; x = cx
            while left <= x:
                x -= 1; ox -= cos; oy += sin
                if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                    find = True
                    cx = x; sx = ox; sy = oy
                    break
        if not find: break

    # 上方向のループ：画面中央から上に向かって走査し、座標は足し算と引き算で計算
    cx = bkcx
    sx = tcx; sy = tcy
    left = cx - tmax; right = cx + tmax
    for y in range(cy-1,0,-1):
        sx -= sin; sy -= cos
        find = False
        if 0 <= sx < tex.get_width() and 0 <= sy < tex.get_height():
            find = True
        # 1. 中心から右へ検索
        if not find and right != None:
            ox = sx; oy = sy; x = cx
            while x <= right:
                x += 1; ox += cos; oy -= sin    # 回転座標を対応してずらす
                if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                    find = True
                    cx = x; sx = ox; sy = oy
                    break
        # 2. 左へ検索
        if not find and left != None:
            ox = sx; oy = sy; x = cx
            while left <= x:
                x -= 1; ox -= cos; oy += sin
                if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                    find = True
                    cx = x; sx = ox; sy = oy
                    break
        if not find: break

        # 右上方向のループ：右上方向に走査し、探索範囲は前行の描画範囲を基に拡張
        ox = sx; oy = sy
        right = None; left = None
        for x in range(cx, cx+tmax):
            if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                col = tex.get_at((int(ox) & 255, int(oy) & 255))
                suf.set_at((x, y), col)
                right = x
            else: break
            ox += cos; oy -= sin
        # 左上方向のループ：左上方向に走査し、探索範囲は前行の描画範囲を基に拡張
        ox = sx; oy = sy
        for x in range(cx-1, cx-tmax, -1):
            ox -= cos; oy += sin
            if 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height():
                col = tex.get_at((int(ox) & 255, int(oy) & 255))
                suf.set_at((x, y), col)
                left = x
            else: break

main()
