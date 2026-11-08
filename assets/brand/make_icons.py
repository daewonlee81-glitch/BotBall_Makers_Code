#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""botball-logo.jpg → 웹앱용 아이콘·섬네일 생성 (이 프로젝트 전용)
필요: pip install pillow numpy scipy   /  한글 글꼴: Noto Sans CJK (og-image 제목용)
실행: python3 make_icons.py   (이 폴더에서)"""
import glob
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = Path(__file__).resolve().parent
src = Image.open(HERE / 'botball-logo.jpg').convert('RGB')

# 1) 왼쪽 Botguy만 잘라내기 ('B' 글자와 TM 표시 제외), 바깥 흰 배경만 투명하게
rob = np.asarray(src.crop((0, 0, 800, 1091))).copy()
rob[:690, 700:] = 255
rob[1000:, 772:] = 255
lum = np.asarray(Image.fromarray(rob).convert('L')).astype(int)
lab, _ = ndimage.label(lum > 235)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
outer = np.isin(lab, list(border))
near = ndimage.binary_dilation(outer, iterations=2)
a = np.dstack([rob, np.full(lum.shape, 255, np.uint8)])
a[outer, 3] = 0
edge = near & ~outer & (lum > 160)
a[edge, 3] = np.clip((255 - lum[edge]) * 255 // 95, 0, 255).astype(np.uint8)
bot = Image.fromarray(a)
bot = bot.crop(bot.getbbox())
bot.save(HERE / 'botguy.png')


def icon(size, pad=0.10, radius=0.22, rounded=True):
    c = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    if rounded:
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius), fill=(255, 255, 255, 255))
    else:
        d.rectangle([0, 0, size, size], fill=(255, 255, 255, 255))
    b = bot.copy()
    inner = int(size * (1 - 2 * pad))
    b.thumbnail((inner, inner), Image.LANCZOS)
    c.alpha_composite(b, ((size - b.width) // 2, (size - b.height) // 2))
    return c


# 2) 아이콘들
icon(512).save(HERE / 'icon-512.png')
icon(192).save(HERE / 'icon-192.png')
icon(180, pad=0.09, rounded=False).convert('RGB').save(HERE / 'apple-touch-icon.png')
icon(64, pad=0.06, radius=0.20).save(HERE / 'favicon-64.png')
icon(32, pad=0.04, radius=0.18).save(HERE / 'favicon-32.png')
icon(96, pad=0.08, radius=0.22).save(HERE / 'header-badge.png')

# 3) 링크 미리보기 이미지 (1200×630)
og = Image.new('RGB', (1200, 630), (255, 255, 255))
logo = src.copy()
logo.thumbnail((760, 330), Image.LANCZOS)
og.paste(logo, ((1200 - logo.width) // 2, 70))
d = ImageDraw.Draw(og)
fonts = glob.glob('/usr/share/fonts/**/NotoSansCJK-Bold.ttc', recursive=True) + \
        glob.glob('/System/Library/Fonts/AppleSDGothicNeo.ttc') + glob.glob('C:/Windows/Fonts/malgunbd.ttf')


def kr(size):
    for fp in fonts:
        for i in range(10):
            try:
                f = ImageFont.truetype(fp, size, index=i)
            except OSError:
                break
            if 'CJK' not in f.getname()[0] or 'KR' in f.getname()[0]:
                return f
    return ImageFont.load_default()


t1, t2 = '웜뱃 블록코딩', 'KIPR Wombat · 블록으로 코딩하고 Python으로 실행'
f1, f2 = kr(78), kr(34)
y = 70 + logo.height + 40
d.text(((1200 - d.textlength(t1, font=f1)) / 2, y), t1, font=f1, fill=(20, 33, 61))
d.text(((1200 - d.textlength(t2, font=f2)) / 2, y + 100), t2, font=f2, fill=(90, 100, 120))
og.save(HERE / 'og-image.png', optimize=True)
print('완료:', ', '.join(sorted(p.name for p in HERE.glob('*.png'))))
