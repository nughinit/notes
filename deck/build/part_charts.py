from lib import *
from flow import NSDECL, _run, _esc
from lxml import etree

def add_subtitle(slide, text):
    """Subtítulo do padrão: logo abaixo do título, 13 pt #737A7F, 1 linha."""
    xml = ('<p:sp %s><p:nvSpPr><p:cNvPr id="900" name="Subtítulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>'
           '<a:xfrm><a:off x="711403" y="1040000"/><a:ext cx="10771632" cy="213167"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
           '<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
           '<a:p><a:pPr algn="l" marL="0" indent="0"><a:buNone/></a:pPr>%s</a:p></p:txBody></p:sp>'
           % (NSDECL, _run(text, 13, '737A7F', False)))
    slide.shapes._spTree.append(etree.fromstring(xml))

def run(prs, S):
    add_subtitle(S[47], 'Desfecho composto: 13,5% no High-Risk contra 0,4% no Low-Risk')
    return {48: [S[47]]}
