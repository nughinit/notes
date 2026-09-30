"""Recortes (sem redesenhar) das ilustrações/ícones das figuras de diretriz."""
from PIL import Image, ImageDraw
import numpy as np, os

OUT = os.path.join(os.path.dirname(__file__), 'crops')
os.makedirs(OUT, exist_ok=True)

def _save(im, name):
    p = os.path.join(OUT, name); im.save(p); return p

def circle_icon(src, box, name):
    im = Image.open(src).convert('RGB').crop(box)
    w, h = im.size; S = 4
    mask = Image.new('L', (w * S, h * S), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, w * S - 1, h * S - 1), fill=255)
    a = mask.resize((w, h), Image.LANCZOS)
    im = im.convert('RGBA'); im.putalpha(a)
    return _save(im, name)

def bg_transparent(src, box, name, ref=None, tol=40, soft=20):
    im = Image.open(src).convert('RGB').crop(box)
    arr = np.asarray(im).astype(int)
    r = arr[ref[1], ref[0]] if ref else arr[0, 0]
    d = np.sqrt(((arr - r) ** 2).sum(axis=2))
    alpha = np.clip((d - tol) / soft, 0, 1) * 255
    out = np.dstack([arr.astype('uint8'), alpha.astype('uint8')])
    return _save(Image.fromarray(out, 'RGBA'), name)

def plain(src, box, name):
    return _save(Image.open(src).convert('RGB').crop(box), name)

def white_flood(src, box, name, tol=28):
    """Torna transparente o branco externo (flood a partir das bordas); mantém brancos internos."""
    im = Image.open(src).convert('RGB').crop(box)
    w, h = im.size
    arr = np.asarray(im).astype(int)
    near = (np.abs(arr - 255).max(axis=2) <= tol)
    seen = np.zeros((h, w), bool)
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y, x] or not near[y, x]: continue
        seen[y, x] = True
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    alpha = np.where(seen, 0, 255).astype('uint8')
    out = np.dstack([arr.astype('uint8'), alpha])
    return _save(Image.fromarray(out, 'RGBA'), name)

def build_all():
    c30 = '/tmp/img_30.jpg'; c33 = '/tmp/img_33.jpg'
    P = {}
    P['pessoa'] = bg_transparent(c30, (172, 316, 236, 430), 'pessoa.png', ref=(3, 40), tol=70)
    P['stetos'] = bg_transparent(c30, (950, 285, 1010, 345), 'stetos.png', ref=(2, 2), tol=60)
    P['cron'] = circle_icon(c30, (624, 517, 708, 599), 'cron.png')
    P['prancheta'] = circle_icon(c30, (624, 764, 708, 846), 'prancheta.png')
    P['pilula'] = circle_icon(c30, (628, 1010, 712, 1094), 'pilula.png')
    P['microscopio'] = circle_icon(c30, (1240, 1008, 1322, 1092), 'microscopio.png')
    P['sirene'] = circle_icon(c30, (125, 1224, 205, 1304), 'sirene.png')
    # rota diagnóstica (fig. 6)
    P['torso'] = plain(c33, (105, 440, 700, 885), 'torso.png')
    P['ecg_eletrodos'] = plain(c33, (840, 333, 1172, 628), 'ecg_eletrodos.png')
    P['us'] = plain(c33, (1222, 333, 1518, 628), 'us.png')
    P['troponina'] = plain(c33, (1597, 333, 1893, 628), 'troponina.png')
    P['ecg_onda'] = bg_transparent(c33, (880, 1052, 1104, 1124), 'ecg_onda.png', ref=(2, 2), tol=60)
    P['stetos2'] = bg_transparent(c33, (1282, 1062, 1376, 1172), 'stetos2.png', ref=(2, 2), tol=60)
    return P

if __name__ == '__main__':
    P = build_all()
    ims = [Image.open(p) for p in P.values()]
    W = sum(i.size[0] for i in ims) + 20 * len(ims); H = max(i.size[1] for i in ims)
    sh = Image.new('RGB', (W, H), '#4E7C8B'); x = 0
    for i in ims:
        sh.paste(i, (x, 0), i if i.mode == 'RGBA' else None); x += i.size[0] + 20
    sh.save(os.path.join(OUT, 'sheet.png'))
    print(P.keys())
