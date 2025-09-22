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
        draw_rotated_texture(suf, tex, cx, cy, math.cos(r), math.sin(r))
        r += 1/256

        clock.tick(60)
        screen.blit(pygame.transform.scale(suf,(w*3,h*3)),(0,0))
        pygame.display.flip()
        pygame.image.save(screen, f"m/{cnt:03d}.png")
        cnt += 1

def draw_rotated_texture(suf, tex, cx, cy, dx, dy):
    tcx = tex.get_width()/2; tcy = tex.get_height()/2  
    sright, sleft = draw_line(suf, tex, tcx, tcy, cx, cy, dx, -dy)
    # 下方向のループ：画面中央から下に向かって走査し、座標は足し算と引き算で計算
    bkcx = cx; sx = tcx; sy = tcy; right = sright; left = sleft
    y = cy + 1
    while True:
        # 次のY座標の開始位置を求める
        sx += dy; sy += dx
        cx, sx, sy = find_next(tex, sx, sy, cx, dx, -dy, right, left)
        if not cx: break
        # 描画
        right, left = draw_line(suf, tex, sx, sy, cx, y, dx, -dy); y += 1
    # 上方向のループ：画面中央から上に向かって走査し、座標は足し算と引き算で計算
    cx = bkcx; sx = tcx; sy = tcy; right = sright; left = sleft
    y = cy - 1
    while True:
        # 次のY座標の開始位置を求める
        sx -= dy; sy -= dx
        cx, sx, sy = find_next(tex, sx, sy, cx, dx, -dy, right, left)
        if not cx: break
        # 描画
        right, left = draw_line(suf, tex, sx, sy, cx, y, dx, -dy); y -= 1

# テクスチャの領域にあるか判定
def in_rect(tex, ox, oy):
    return 0 <= ox < tex.get_width() and 0 <= oy < tex.get_height()

# 次の描画位置を sx, sy から right,sy - left, sy の間で検索する
def find_next(tex, sx, sy, cx, dx, dy, right, left):
    if in_rect(tex, sx, sy): return (cx, sx, sy)
    if right != None: # 右へ検索
        ox = sx; oy = sy; x = cx
        while x <= right:
            x += 1; ox += dx; oy += dy    # 回転座標を対応してずらす
            if in_rect(tex, ox, oy): return (x, ox, oy)
    if left != None: # 左へ検索
        ox = sx; oy = sy; x = cx
        while left <= x:
            x -= 1; ox -= dx; oy -= dy
            if in_rect(tex, ox, oy): return (x, ox, oy)
    return (None,0,0)

# テクスチャの領域にあればその点を描画する
def set_in_rect(suf, tex, ox, oy, x, y):
    if in_rect(tex, ox, oy):
        suf.set_at((x, y), tex.get_at((int(ox), int(oy))))
        return True
    return False

# 左側に描画
def draw_right(suf, tex, sx, sy, x, y, dx, dy):
    lastx = None
    while True:
        if not set_in_rect(suf, tex, sx, sy, x, y): return lastx
        lastx = x; sx += dx; sy += dy; x += 1

# 右側に描画
def draw_left(suf, tex, sx, sy, x, y, dx, dy):
    lastx = None
    while True:
        x -= 1; sx += dx; sy += dy
        if not set_in_rect(suf, tex, sx, sy, x, y): return lastx
        lastx = x

# １ライン描画
def draw_line(suf, tex, sx, sy, x, y, dx, dy):
    return (draw_right(suf, tex, sx, sy, x, y, dx, dy),
            draw_left(suf, tex, sx, sy, x, y, -dx, -dy))

main()
