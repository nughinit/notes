"""Construtor de fluxogramas no padrão (formas nativas, setas ortogonais contínuas)."""
from lxml import etree
from lib import *

TEAL, TEAL_M, AQUA, GRAF, CINZA = '4E7C8B', '6E9DAB', '8EC4CB', '6B6E70', 'A3A6A8'
BRANCO, SURF, TITULO, TINTA, APOIO = 'FBFCFC', 'F2F4F5', '3B3F42', '1F3238', '737A7F'

NSDECL = 'xmlns:a="%s" xmlns:p="%s" xmlns:r="%s"' % (A, P, R)

def _esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _run(txt, sz, color, medium):
    face = 'Roboto Medium' if medium else 'Roboto'
    return ('<a:r><a:rPr lang="pt-BR" sz="%d" b="0" i="0" dirty="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
            '<a:latin typeface="%s"/><a:ea typeface="%s"/><a:cs typeface="%s"/></a:rPr><a:t>%s</a:t></a:r>'
            % (sz * 100, color, face, face, face, _esc(txt)))

def _paras(lines, sz, color, medium, algn):
    return ''.join('<a:p><a:pPr algn="%s"/>%s</a:p>' % (algn, _run(l, sz, color, medium)) for l in lines)

class Flow:
    def __init__(self, slide, first_id=300):
        self.slide = slide
        self.tree = slide.shapes._spTree
        self.n = first_id
        self.shapes = {}   # nome lógico -> (x, y, w, h)

    def _add(self, xml):
        el = etree.fromstring(xml)
        self.tree.append(el)
        return el

    def _id(self):
        self.n += 1
        return self.n

    def _box(self, name, prst, fill, ln, x, y, w, h, lines, sz, color, key=None, adj=None, ins=91440):
        sid = self._id()
        av = '<a:avLst><a:gd name="adj" fmla="val 50000"/></a:avLst>' if adj else '<a:avLst/>'
        lnx = ('<a:ln w="12700"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % ln) if ln else '<a:ln><a:noFill/></a:ln>'
        xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>'
               '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="%s">%s</a:prstGeom>'
               '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>%s<a:effectLst/></p:spPr>'
               '<p:txBody><a:bodyPr rtlCol="0" anchor="ctr" wrap="square" lIns="%d" rIns="%d" tIns="45720" bIns="45720"/><a:lstStyle/>%s</p:txBody></p:sp>'
               % (NSDECL, sid, _esc(name), x, y, w, h, prst, av, fill, lnx, ins, ins,
                  _paras(lines, sz, color, True, 'ctr')))
        self._add(xml)
        if key: self.shapes[key] = (x, y, w, h)
        return (x, y, w, h)

    def pill(self, x, y, w, h, lines, key=None):
        return self._box('Fim/Início', 'roundRect', TEAL, None, x, y, w, h, lines, 13, BRANCO, key, adj=True)

    def step(self, x, y, w, h, lines, key=None):
        return self._box('Etapa', 'rect', SURF, TEAL_M, x, y, w, h, lines, 13, TITULO, key)

    def diamond(self, x, y, w, h, lines, key=None):
        return self._box('Decisão', 'diamond', AQUA, None, x, y, w, h, lines, 12, TINTA, key, ins=0)

    def label(self, x, y, text, w=E(0.55), algn='l', color=TEAL, medium=True):
        sid = self._id()
        xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Rótulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>'
               '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
               '<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>'
               % (NSDECL, sid, x, y, w, E(0.22), _paras([text], 12, color, medium, algn)))
        self._add(xml)

    def arrow(self, pts, dash=False, name='Seta'):
        """Polilinha ortogonal contínua com ponta no último ponto."""
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, y0 = min(xs), min(ys)
        w, h = max(max(xs) - x0, 1), max(max(ys) - y0, 1)
        path = '<a:moveTo><a:pt x="%d" y="%d"/></a:moveTo>' % (pts[0][0] - x0, pts[0][1] - y0)
        path += ''.join('<a:lnTo><a:pt x="%d" y="%d"/></a:lnTo>' % (px - x0, py - y0) for px, py in pts[1:])
        sid = self._id()
        d = '<a:prstDash val="dash"/>' if dash else ''
        xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>'
               '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
               '<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>'
               '<a:pathLst><a:path w="%d" h="%d" fill="none">%s</a:path></a:pathLst></a:custGeom><a:noFill/>'
               '<a:ln w="19050"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>%s<a:round/><a:tailEnd type="triangle" w="med" len="med"/></a:ln>'
               '<a:effectLst/></p:spPr></p:sp>' % (NSDECL, sid, name, x0, y0, w, h, w, h, path, GRAF, d))
        self._add(xml)

def set_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    tf.text = text if not tf.text.strip() else tf.text.rstrip() + '\n\n' + text

def by_name(slide, name):
    return [el for el in slide.shapes._spTree if el.tag == q('p:sp') and el.find('.//p:cNvPr', NS).get('name') == name]

def remove_flow_shapes(slide, keep_names=()):
    """Remove formas/conectores/rótulos do fluxo antigo; preserva título, rodapé, logo e `keep_names`."""
    for el in list(slide.shapes._spTree):
        if el.tag not in (q('p:sp'), q('p:pic'), q('p:graphicFrame'), q('p:cxnSp'), q('p:grpSp')): continue
        nm = el.find('.//p:cNvPr', NS).get('name')
        if is_chrome(el) or nm in keep_names: continue
        el.getparent().remove(el)


# ======================================================================
# Extensões para a seção G (refazer figuras de diretriz como nativas)
# ======================================================================
SEM = {'in': ('B5533C', BRANCO), 'obs': ('C98A2B', TINTA), 'out': ('3E8E68', BRANCO)}
CORPO = '5F6468'

def _paras_rich(paras, algn):
    """paras: lista de (texto, tamanho_pt, medium, cor, bullet?)"""
    out = []
    for p in paras:
        txt, sz, med, col = p[:4]
        bullet = len(p) > 4 and p[4]
        ppr = '<a:pPr algn="%s"%s>' % (algn, ' marL="171450" indent="-171450"' if bullet else '')
        if bullet:
            ppr += '<a:buClr><a:srgbClr val="%s"/></a:buClr><a:buFont typeface="Roboto"/><a:buChar char="•"/>' % TEAL
        else:
            ppr += '<a:buNone/>'
        ppr += '</a:pPr>'
        out.append('<a:p>%s%s</a:p>' % (ppr, _run(txt, sz, col, med)))
    return ''.join(out)

class GFlow(Flow):
    def gbox(self, kind, x, y, w, h, paras, algn='ctr', anchor='ctr', key=None):
        """kind: pill | step | diamond | in | obs | out | card. paras: (txt, sz, medium, cor[, bullet])."""
        sid = self._id()
        if kind == 'pill':
            prst, fill, ln, adj = 'roundRect', TEAL, None, True
        elif kind == 'step':
            prst, fill, ln, adj = 'rect', SURF, TEAL_M, False
        elif kind == 'diamond':
            prst, fill, ln, adj = 'diamond', AQUA, None, False
        elif kind == 'tealrect':
            prst, fill, ln, adj = 'rect', TEAL, None, False
        else:
            prst, fill, ln, adj = 'rect', SEM[kind][0], None, False
        av = '<a:avLst><a:gd name="adj" fmla="val 50000"/></a:avLst>' if adj else '<a:avLst/>'
        lnx = ('<a:ln w="12700"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % ln) if ln else '<a:ln><a:noFill/></a:ln>'
        ins = 0 if kind == 'diamond' else 91440
        name = {'pill': 'Fim/Início', 'step': 'Etapa', 'diamond': 'Decisão'}.get(kind, 'Status')
        xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>'
               '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="%s">%s</a:prstGeom>'
               '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>%s<a:effectLst/></p:spPr>'
               '<p:txBody><a:bodyPr rtlCol="0" anchor="%s" wrap="square" lIns="%d" rIns="%d" tIns="45720" bIns="45720"/><a:lstStyle/>%s</p:txBody></p:sp>'
               % (NSDECL, sid, name, x, y, w, h, prst, av, fill, lnx, anchor, ins, ins, _paras_rich(paras, algn)))
        self._add(xml)
        if key: self.shapes[key] = (x, y, w, h)
        return (x, y, w, h)

    def text(self, x, y, w, h, paras, algn='l', name='Texto', anchor='t'):
        sid = self._id()
        xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>'
               '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
               '<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="%s"><a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>'
               % (NSDECL, sid, name, x, y, w, h, anchor, _paras_rich(paras, algn)))
        self._add(xml)

    def card(self, x, y, w, h, title, paras):
        """Card do padrão (Superfície + faixa de 3 pt Teal Profundo) com título 15 pt e corpo."""
        sid = self._id()
        self._add('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Card"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
                  '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:ln><a:noFill/></a:ln><a:effectLst/></p:spPr></p:sp>' % (NSDECL, self._id(), x, y, w, h, SURF))
        self._add('<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Faixa"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
                  '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:ln><a:noFill/></a:ln><a:effectLst/></p:spPr></p:sp>' % (NSDECL, self._id(), x, y, w, 38100, TEAL))
        self.text(x + 228600, y + 182880, w - 457200, 260000, [(title, 15, True, TITULO)], name='Título do card')
        self.text(x + 228600, y + 182880 + 340000, w - 457200, h - 182880 - 340000 - 100000, paras, name='Corpo do card')

    def pic(self, path, x, y, w=None, h=None, descr=''):
        from PIL import Image
        iw, ih = Image.open(path).size
        if w and not h: h = int(w * ih / iw)
        if h and not w: w = int(h * iw / ih)
        pic = self.slide.shapes.add_picture(path, x, y, w, h)
        pic._element.find('.//p:cNvPr', NS).set('descr', descr)
        pic._element.find('.//p:cNvPr', NS).set('name', 'Figura')
        return pic
