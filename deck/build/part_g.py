"""Seção G – figuras de diretriz refeitas como fluxogramas nativos."""
import copy
from lib import *
from flow import *
import crops

CX = 6097219
X0, X1 = 711403, 11483035
PALE = 'E4EEF0'
_C = None

def C():
    global _C
    if _C is None: _C = crops.build_all()
    return _C

# atalhos de parágrafos --------------------------------------------------
def hp(t):  return (t, 13, True, BRANCO)      # título em pílula/teal
def dp(t):  return (t, 12, False, PALE)       # descrição em pílula/teal
def hs(t):  return (t, 13, True, TITULO)      # título em etapa
def ds(t, b=False): return (t, 12, False, CORPO, b)   # descrição em etapa
def dq(t):  return (t, 12, True, TINTA)       # texto de decisão
def sm(kind, t, med=True, sz=13): return (t, sz, med, SEM[kind][1])
def plain(t, b=False, med=False): return (t, 12, med, CORPO, b)

# ---------------------------------------------------------------- estrutura
def to_native_series(prs, src, titles, first_notes=None):
    """Converte um slide-imagem em N slides nativos (layout Título e conteúdo, título no placeholder)."""
    layout = [l for l in prs.slide_layouts if l.name == 'Título e conteúdo'][0]
    for rel in src.part.rels.values():
        if rel.reltype.endswith('/slideLayout'):
            rel._target = layout.part
    # remove a imagem (e solta a relação)
    for pic in list(src.shapes._spTree.iter(q('p:pic'))):
        rid = pic.find('.//a:blip', NS).get(q('r:embed'))
        pic.getparent().remove(pic)
        src.part.drop_rel(rid)
    # título (placeholder) copiado do slide 29
    tmpl = TITLE_TEMPLATE
    slides = [src] + [dup_slide(prs, src) for _ in titles[1:]]
    ref = src
    for s in slides[1:]:
        move_after(prs, s, ref); ref = s
    for s in slides[1:]:
        if s.has_notes_slide: s.notes_slide.notes_text_frame.text = ''
    for s, t in zip(slides, titles):
        el = copy.deepcopy(tmpl)
        ts = list(el.iter(q('a:t')))
        ts[0].text = t
        for x in ts[1:]: x.getparent().getparent().remove(x.getparent())
        s.shapes._spTree.insert(2, el)
    return slides

def title_nlines(s): return title_lines(s)

def top_y(s):
    return E(1.55) if title_lines(s) == 1 else E(1.85)

def frame(s):
    """Retorna GFlow e limpa qualquer forma que não seja título/rodapé/logo."""
    return GFlow(s, first_id=300)

def notes(s, text):
    tf = s.notes_slide.notes_text_frame
    tf.text = text if not tf.text.strip() else tf.text.rstrip() + '\n\n' + text

def arrow_mid(f, pts, dash=False): f.arrow([(int(x), int(y)) for x, y in pts], dash=dash)

def I(v): return E(v)

# ---------------------------------------------------------------- FIGURA A
def figA(prs, src):
    titles = ['Figura Central – Atendimento na emergência (%d/4)' % i for i in (1, 2, 3, 4)]
    S = to_native_series(prs, src, titles)
    P = C()
    # ---- A1
    s = S[0]; f = frame(s)
    f.gbox('pill', I(0.78), I(1.6), I(4.4), I(0.85), [hp('SINTOMAS SUSPEITOS'), dp('(BUSCAR ATENDIMENTO IMEDIATAMENTE)')])
    f.pic(P['pessoa'], I(0.95), I(1.68), h=I(0.7), descr='Pessoa com dor no peito (ilustração recortada da figura original)')
    cx = 7.8
    f.gbox('pill', I(cx - 2.2), I(1.6), I(4.4), I(0.85), [hp('Suspeita clínica confirmada'), dp('(dor torácica ou sintoma equivalente)')])
    arrow_mid(f, [(I(cx), I(2.45)), (I(cx), I(2.75))])
    f.gbox('step', I(cx - 2.2), I(2.75), I(4.4), I(0.8), [hs('PASSO 1'), ds('(Realizar ECG até 10 minutos)')])
    f.pic(P['cron'], I(cx - 2.2 - 0.75), I(2.85), h=I(0.6), descr='Ícone de cronômetro')
    arrow_mid(f, [(I(cx), I(3.55)), (I(cx), I(3.85))])
    f.diamond(I(cx - 1.9), I(3.85), I(3.8), I(1.55), ['ECG COM', 'CRITÉRIOS', 'DIAGNÓSTICOS?'])
    cy = 3.85 + 1.55 / 2
    f.gbox('step', I(10.3), I(cy - 0.8), I(2.26), I(1.6), [hs('SEGUIR ROTA TERAPÊUTICA'), ds('(diretriz específica de acordo com o diagnóstico estabelecido)')])
    arrow_mid(f, [(I(cx + 1.9), I(cy)), (I(10.3), I(cy))])
    f.label(I(cx + 1.95), I(cy - 0.28), 'Sim', w=I(0.45))
    f.gbox('pill', I(1.2), I(5.75), I(3.6), I(0.66), [hp('PASSO 2')])
    arrow_mid(f, [(I(cx - 1.9), I(cy)), (I(3.0), I(cy)), (I(3.0), I(5.75))])
    f.label(I(cx - 1.9 - 0.6), I(cy - 0.28), 'Não', w=I(0.5), algn='r')
    # ---- A2
    s = S[1]; f = frame(s)
    cx = 6.9
    f.gbox('step', I(cx - 2.2), I(1.6), I(4.4), I(0.8), [hs('PASSO 2'), ds('(Avaliação inicial da rota diagnóstica)')])
    f.pic(P['prancheta'], I(cx - 2.2 - 0.75), I(1.7), h=I(0.6), descr='Ícone de prancheta')
    arrow_mid(f, [(I(cx), I(2.4)), (I(cx), I(2.7))])
    f.diamond(I(cx - 1.9), I(2.7), I(3.8), I(1.55), ['HÁ CRITÉRIO DE', 'INSTABILIDADE?¹'])
    cy = 2.7 + 1.55 / 2
    f.gbox('step', I(9.4), I(1.6), I(3.16), I(2.85), [hs('SEGUIR ROTA DE PACIENTE INSTÁVEL:'),
        ds('Avaliação clínica + dosagem de troponina'), ds('Repetir ECG a cada 10-20 minutos (apoio de médico experiente)'),
        ds('Buscar ativamente diagnósticos diferenciais (POCUS, outros exames)'), ds('Admissão na unidade'),
        ds('Tratar conforme diagnóstico estabelecido'), ds('Avaliar indicação de time de choque')], algn='l', anchor='t')
    arrow_mid(f, [(I(cx + 1.9), I(cy)), (I(9.4), I(cy))])
    f.label(I(cx + 1.95), I(cy - 0.28), 'Sim', w=I(0.45))
    f.gbox('pill', I(1.2), I(4.75), I(3.6), I(0.66), [hp('PASSO 3')])
    arrow_mid(f, [(I(cx - 1.9), I(cy)), (I(3.0), I(cy)), (I(3.0), I(4.75))])
    f.label(I(cx - 1.9 - 0.6), I(cy - 0.28), 'Não', w=I(0.5), algn='r')
    f.card(I(5.3), I(4.75), I(7.26), I(1.85), '1. CRITÉRIOS DE INSTABILIDADE:',
           [plain('ECG limítrofe', True), plain('Dor persistente', True), plain('Instabilidade hemodinâmica/Má perfusão (perda de consciência, etc)', True),
            plain('Congestão pulmonar aguda', True), plain('Taquiarritmia / bradiarritmia no cenário de dor torácica aguda', True)])
    f.pic(P['sirene'], I(11.7), I(4.95), h=I(0.62), descr='Ícone de sirene')
    # ---- A3
    s = S[2]; f = frame(s)
    cx = 6.9
    f.gbox('step', I(cx - 2.5), I(1.6), I(5.0), I(1.25), [hs('PASSO 3'), ds('(Decisão após avaliação clínica detalhada com apoio de algoritmos e exames iniciais conforme suspeita clínica)')])
    f.pic(P['pilula'], I(cx - 2.5 - 0.75), I(1.9), h=I(0.6), descr='Ícone de cápsula')
    f.pic(P['microscopio'], I(cx + 2.5 + 0.15), I(1.9), h=I(0.6), descr='Ícone de microscópio')
    arrow_mid(f, [(I(cx), I(2.85)), (I(cx), I(3.15))])
    f.diamond(I(cx - 1.9), I(3.15), I(3.8), I(1.5), ['DIAGNÓSTICO', 'ESTABELECIDO?'])
    cy = 3.15 + 0.75
    f.gbox('pill', I(9.6), I(cy - 0.33), I(2.96), I(0.66), [hp('SEGUIR ROTA TERAPÊUTICA')])
    arrow_mid(f, [(I(cx + 1.9), I(cy)), (I(9.6), I(cy))])
    f.label(I(cx + 1.95), I(cy - 0.28), 'Sim', w=I(0.45))
    f.gbox('pill', I(0.9), I(5.3), I(4.4), I(0.95), [hp('CLASSIFICAR CONFORME ALGORITMOS DE TROPONINA E ESCORES DE RISCO')])
    arrow_mid(f, [(I(cx - 1.9), I(cy)), (I(3.1), I(cy)), (I(3.1), I(5.3))])
    f.label(I(cx - 1.9 - 0.6), I(cy - 0.28), 'Não', w=I(0.5), algn='r')
    # ---- A4
    s = S[3]; f = frame(s)
    cw = 3.58; gap = 0.5; xs = [0.78 + i * (cw + gap) for i in range(3)]
    f.gbox('pill', I(6.67 - 2.9), I(1.6), I(5.8), I(0.85), [hp('CLASSIFICAR CONFORME ALGORITMOS DE TROPONINA E ESCORES DE RISCO')])
    f.pic(P['microscopio'], I(6.67 + 2.9 + 0.15), I(1.72), h=I(0.6), descr='Ícone de microscópio')
    cents = [x + cw / 2 for x in xs]
    for c in cents:
        arrow_mid(f, [(I(6.67), I(2.45)), (I(6.67), I(2.8)), (I(c), I(2.8)), (I(c), I(3.1))])
    f.gbox('in', I(xs[0]), I(3.1), I(cw), I(1.3), [sm('in', 'RULE IN – ADMISSÃO DO PACIENTE')])
    f.gbox('obs', I(xs[1]), I(3.1), I(cw), I(1.3), [sm('obs', 'PASSO 4'), sm('obs', '(Observação e investigação adicional nos casos de probabilidade/risco intermediário)', False, 12)])
    f.gbox('out', I(xs[2]), I(3.1), I(cw), I(1.3), [sm('out', 'RULE OUT – DESCARTE DO DIAGNÓSTICO DE IAM')])
    f.text(I(xs[0]), I(4.55), I(cw), I(1.3), [plain('Avaliar critérios de IAM e, na ausência de critérios de IAM, buscar ativamente a causa da injúria')])
    f.text(I(xs[1]), I(4.55), I(cw), I(1.3), [plain('Solicitar terceira dosagem de troponina, repetir ECG, realizar mais escores de risco (ex: GRACE) e considerar exames adicionais conforme suspeita*')])
    f.text(I(xs[2]), I(4.55), I(cw), I(1.3), [plain('Na ausência de diagnósticos alternativos para a causa da dor torácica, considerar alta para casa, especialmente se HEART score <4 em paciente sem antecedente de doença coronária*')])
    f.text(I(0.78), I(6.15), I(11.78), I(0.25), [(  '*Se suspeita de SCA persistir, seguir fluxo de investigação não-invasiva (figuras 13 e 14)', 12, False, APOIO)], name='Nota')
    return S

def subtitle(s, text):
    import part_charts
    part_charts.add_subtitle(s, text)

FOOT = lambda t: (t, 12, False, APOIO)

# ---------------------------------------------------------------- FIGURA B (rota diagnóstica – fig. 6)
def figB(prs, src):
    titles = ['Rota diagnóstica – ECG inicial não-diagnóstico (%d/2)' % i for i in (1, 2)]
    S = to_native_series(prs, src, titles)
    P = C()
    for k, s in enumerate(S):
        f = frame(s)
        subtitle(s, 'Figura 6 – Passo 2: avaliação inicial da rota diagnóstica.')
        f.pic(P['torso'], I(0.98), I(1.6), w=I(3.0), descr='Paciente com dor torácica (ilustração recortada da figura original)')
        dy, dh = 3.95, 2.5
        f.diamond(I(0.78), I(dy), I(4.4), I(dh), ['ECG LIMÍTROFE/', 'DUVIDOSO OU', 'CRITÉRIOS DE', 'INSTABILIDADE CLÍNICA', '(incluindo dor persistente)?'])
        cy = dy + dh / 2
        f.text(I(5.9), I(6.32), I(6.66), I(0.25), [FOOT('*Algoritmos de troponina conforme figuras 11A e 11B')], name='Nota')
        if k == 0:
            xs = [5.9, 8.25, 10.6]; w = 1.96
            imgs = [('ecg_eletrodos', 'Eletrodos de ECG no tórax (ilustração recortada)'), ('us', 'Ecocardiograma no monitor (ilustração recortada)'), ('troponina', 'Tubo de coleta de sangue (ilustração recortada)')]
            for x, (key, d) in zip(xs, imgs):
                f.pic(P[key], I(x + w / 2 - 0.65), I(1.55), h=I(1.25), descr=d)
            f.gbox('step', I(xs[0]), I(2.95), I(w), I(3.25), [hs('REPETIR ECG A CADA 10-20 MINUTOS'), ds('(apoio de médico experiente),'),
                   hs('MANTER MONITORIZAÇÃO E TRATAR CRITÉRIOS DE INSTABILIDADE'), ds('(acionar time de choque se instabilidade hemodinâmica)')], algn='l', anchor='t')
            f.gbox('step', I(xs[1]), I(2.95), I(w), I(3.25), [hs('BUSCAR ATIVAMENTE OUTROS DIAGNÓSTICOS'), ds('avaliação clínica detalhada', True), ds('uso de escores diagnósticos', True),
                   ds('RX', True), ds('POCUS', True), ds('outros exames conforme suspeita', True)], algn='l', anchor='t')
            f.gbox('step', I(xs[2]), I(2.95), I(w), I(1.4), [hs('ALGORITMOS DE TROPONINA*')], algn='l', anchor='t')
            for xm in (xs[0] + w + 0.17, xs[1] + w + 0.17):
                f.text(I(xm - 0.1), I(4.4), I(0.2), I(0.3), [('+', 15, True, TEAL)], algn='ctr', name='Rótulo')
            f.arrow([(I(5.18), I(cy)), (I(5.72), I(cy)), (I(5.72), I(4.5)), (I(xs[0]), I(4.5))])
            f.label(I(5.24), I(cy - 0.28), 'Sim', w=I(0.4))
        else:
            f.gbox('tealrect', I(5.9), I(3.6), I(2.85), I(2.4), [hp('REPETIR ECG SE PIORA CLÍNICA'), dp('(imediatamente)')], anchor='b')
            f.pic(P['ecg_onda'], I(5.9 + 0.45), I(3.7), w=I(1.95), descr='Traçado de ECG (ícone recortado)')
            f.gbox('tealrect', I(9.25), I(3.6), I(3.31), I(2.4), [hp('AVALIAÇÃO CLÍNICA DETALHADA'), dp('(incluindo escores clínicos)'),
                   hp('E ALGORITMOS DE TROPONINA*'), dp('(outros exames conforme suspeita diagnóstica)')], anchor='b')
            f.text(I(8.75), I(4.65), I(0.5), I(0.3), [('+', 15, True, TEAL)], algn='ctr', name='Rótulo')
            f.pic(P['stetos2'], I(9.25 + 1.4), I(3.68), h=I(0.7), descr='Estetoscópio (ícone recortado)')
            f.arrow([(I(5.18), I(cy)), (I(5.72), I(cy)), (I(5.72), I(4.8)), (I(5.9), I(4.8))])
            f.label(I(5.22), I(cy - 0.28), 'Não', w=I(0.45))
    return S

# ---------------------------------------------------------------- FIGURAS C e D (troponina)
DESC_IN = 'Avaliar critérios de IAM e, na ausência de critérios de IAM, buscar ativamente a causa da injúria'
DESC_OUT = 'Na ausência de diagnósticos alternativos para a causa da dor torácica, considerar alta para casa, especialmente se HEART score <4 em paciente sem antecedente de doença coronária *'
DESC_OBS = 'Solicitar terceira dosagem de troponina, repetir ECG, realizar escores de risco e considerar exames adicionais conforme suspeita*'

def trop(prs, src, title, badge, badge_note, d1, d3lines, new_box, foot, two_hour):
    DESC_OUT_ = DESC_OUT if two_hour else DESC_OUT.replace('coronária *', 'coronária*')
    titles = ['%s (%d/2)' % (title, i) for i in (1, 2)]
    S = to_native_series(prs, src, titles)
    # ---- 1/2
    s = S[0]; f = frame(s); ty = 1.85
    f.gbox('pill', I(0.78), I(ty), I(2.4), I(0.5), [hp(badge)])
    if badge_note:
        f.text(I(0.78), I(2.5), I(3.6), I(0.8), [FOOT(badge_note)], name='Nota')
    f.gbox('step', I(5.9), I(ty), I(3.6), I(0.5), [hs('Coletar na admissão (0h)')])
    arrow_mid(f, [(I(7.7), I(ty + 0.5)), (I(7.7), I(2.6))])
    f.diamond(I(5.8), I(2.6), I(3.8), I(1.2), d1)
    cy1 = 3.2
    f.gbox('in', I(10.2), I(2.83), I(2.36), I(0.75), [sm('in', 'RULE IN – ADMISSÃO DO PACIENTE', True, 12)])
    f.text(I(10.2), I(3.68), I(2.36), I(0.85), [plain(DESC_IN)])
    arrow_mid(f, [(I(9.6), I(cy1)), (I(10.2), I(cy1))])
    f.label(I(9.66), I(cy1 - 0.28), 'Sim', w=I(0.45))
    f.diamond(I(3.0), I(3.95), I(4.0), I(2.0), ['Tempo do sintoma', '> 3h e valor', 'muito baixo', 'de TCas', '(indetectável)?'])
    cy2 = 4.95
    arrow_mid(f, [(I(5.8), I(cy1)), (I(5.0), I(cy1)), (I(5.0), I(3.95))])
    f.label(I(5.2), I(cy1 - 0.28), 'Não', w=I(0.5), algn='r')
    f.gbox('out', I(7.7), I(cy2 - 0.4), I(2.4), I(0.8), [sm('out', 'RULE OUT – DESCARTE DO DIAGNÓSTICO DE IAM', True, 12)])
    f.text(I(10.3), I(cy2 - 0.25), I(2.26), I(1.5), [plain(DESC_OUT_)])
    arrow_mid(f, [(I(7.0), I(cy2)), (I(7.7), I(cy2))])
    f.label(I(7.05), I(cy2 - 0.28), 'Sim', w=I(0.45))
    f.gbox('step', I(0.78), I(cy2 - 0.7), I(1.5), I(1.4), [hs(new_box[0])])
    arrow_mid(f, [(I(3.0), I(cy2)), (I(2.28), I(cy2))])
    f.label(I(2.32), I(cy2 - 0.28), 'Não', w=I(0.5))
    f.text(I(0.78), I(6.25), I(11.78), I(0.42), [FOOT(foot)], name='Nota')
    # ---- 2/2
    s = S[1]; f = frame(s)
    f.gbox('pill', I(0.78), I(ty), I(2.4), I(0.5), [hp(badge)])
    f.gbox('step', I(4.97), I(ty), I(3.4), I(0.6), [hs(new_box[0])])
    arrow_mid(f, [(I(6.67), I(ty + 0.6)), (I(6.67), I(2.75))])
    f.diamond(I(4.77), I(2.75), I(3.8), I(1.8), d3lines)
    cy = 3.65
    if two_hour:
        f.gbox('in', I(0.78), I(3.25), I(3.1), I(0.8), [sm('in', 'RULE IN – ADMISSÃO DO PACIENTE', True, 12)])
        f.text(I(0.78), I(4.15), I(3.1), I(1.3), [plain(DESC_IN)])
        arrow_mid(f, [(I(4.77), I(cy)), (I(3.88), I(cy))])
        f.text(I(2.1), I(cy - 0.62), I(2.6), I(0.5), [('Níveis elevados e/ou com delta', 12, False, TITULO)], algn='r', name='Rótulo')
        f.gbox('out', I(9.3), I(3.25), I(3.26), I(0.8), [sm('out', 'RULE OUT – DESCARTE DO DIAGNÓSTICO DE IAM', True, 12)])
        f.text(I(9.3), I(4.15), I(3.26), I(1.5), [plain(DESC_OUT_)])
        arrow_mid(f, [(I(8.57), I(cy)), (I(9.3), I(cy))])
        f.text(I(8.6), I(cy - 0.62), I(2.0), I(0.5), [('Níveis baixos e sem delta', 12, False, TITULO)], name='Rótulo')
        f.gbox('obs', I(5.07), I(5.0), I(3.2), I(0.55), [sm('obs', 'OBSERVAÇÃO', True, 13)])
        arrow_mid(f, [(I(6.67), I(4.55)), (I(6.67), I(5.0))])
        f.text(I(6.8), I(4.62), I(2.2), I(0.3), [('Níveis intermediários', 12, False, TITULO)], name='Rótulo')
        f.text(I(4.47), I(5.6), I(4.4), I(0.6), [plain(DESC_OBS)], algn='ctr')
    else:
        f.gbox('out', I(0.78), I(3.25), I(3.1), I(0.8), [sm('out', 'RULE OUT – DESCARTE DO DIAGNÓSTICO DE IAM', True, 12)])
        f.text(I(0.78), I(4.15), I(3.1), I(1.6), [plain(DESC_OUT_)])
        arrow_mid(f, [(I(4.77), I(cy)), (I(3.88), I(cy))])
        f.label(I(4.2), I(cy - 0.28), 'Não', w=I(0.5), algn='r')
        f.gbox('in', I(9.3), I(3.25), I(3.26), I(0.8), [sm('in', 'RULE IN – ADMISSÃO DO PACIENTE', True, 12)])
        f.text(I(9.3), I(4.15), I(3.26), I(1.3), [plain(DESC_IN)])
        arrow_mid(f, [(I(8.57), I(cy)), (I(9.3), I(cy))])
        f.label(I(8.62), I(cy - 0.28), 'Sim', w=I(0.45))
    f.text(I(0.78), I(6.25), I(11.78), I(0.42), [FOOT(foot)], name='Nota')
    return S

def figC(prs, src):
    return trop(prs, src, 'Fluxos 0-1h e 0-2h – Troponina cardíaca de alta sensibilidade (TCas)', 'PRIMEIRA ESCOLHA', None,
                ['Nível elevado', '(Tabela 26)?'], ['Conduta', 'conforme', 'tabela 26'], ['Realizar novas coletas em 1 ou 2 horas*'],
                '*Se suspeita de SCA persistir, seguir fluxo de investigação não-invasiva (ver tópico 4.3.3 e figuras 13 e 14). Na impossibilidade de realizar coleta em 1 ou 2 horas, coletar em 3 horas (ver figura 11B).', True)

def figD(prs, src):
    return trop(prs, src, 'Fluxo 0-3h – Troponina cardíaca de alta sensibilidade (TCas)', 'SEGUNDA ESCOLHA',
                'Alternativa a ser considerada quando não for possível realizar algoritmos de 0/1h ou 0/2h',
                ['Valor > 5x', 'percentil 99?'], ['Acima do', 'percentil 99', 'e variação', '>20%?'], ['Realizar nova coleta em 3 horas'],
                '*Se suspeita de SCA persistir, seguir fluxo de investigação não-invasiva (ver tópico 4.3.3 e figuras 13 e 14).', False)

# ---------------------------------------------------------------- FIGURA E (ADD-RS – fig. 9)
LEG9 = 'Figura 9 – Fluxograma para investigação de síndrome aórtica aguda.'
NOTE9 = '*Casos suspeitos com sinais radiográficos sugestivos de dissecção de aorta (ex: alargamento de mediastino), seguir fluxo de alta probabilidade.'
ECGBOX = ['Realizar ECG e POCUS/Radiografia de tórax*', '(quando disponível)']

def figE(prs, src):
    titles = ['Escore de risco para detecção de dissecção de aorta (ADD-RS) (%d/3)' % i for i in (1, 2, 3)]
    S = to_native_series(prs, src, titles)
    ty = 1.85
    # ---- E1
    s = S[0]; f = frame(s)
    xs = [0.78, 4.82, 8.86]; w = 3.7
    f.gbox('step', I(xs[0]), I(ty), I(w), I(2.3), [hs('CONDIÇÃO DE ALTO RISCO'), ds('Síndrome de Marfan ou outra doença do tecido conjuntivo', True), ds('História familiar de doença de aorta', True),
        ds('Doença valvar aórtica conhecida', True), ds('Manipulação aórtica recente', True), ds('Aneurisma de aorta torácica conhecido', True)], algn='l', anchor='t')
    f.gbox('step', I(xs[1]), I(ty), I(w), I(2.3), [hs('CARACTERÍSTICAS DA DOR DE ALTO RISCO'), ds('Dor torácica, em dorso ou abdominal conforme descrição a seguir:'),
        ds('Início abrupto', True), ds('Intensa', True), ds('Rasgante', True)], algn='l', anchor='t')
    f.gbox('step', I(xs[2]), I(ty), I(w), I(2.3), [hs('ACHADOS DE ALTO RISCO EM EXAMES'), ds('Sinais de má perfusão orgânica:'), ds('Assimetria de pulso', True), ds('Assimetria de pressão arterial', True),
        ds('Déficit neurológico focal', True), ds('Sopro de insuficiência aórtica (novo ou desconhecido)'), ds('Hipotensão ou choque')], algn='l', anchor='t')
    f.gbox('step', I(0.78), I(4.4), I(3.3), I(1.5), [hs('Avaliação pelo POCUS:'), ds('Sinais diretos: Presença de Flap, hematoma ou úlcera'),
        ds('Sinais indiretos: Dilatação de aorta, derrame pericárdico ou insuficiência valvar aórtica')], algn='l', anchor='t')
    f.gbox('step', I(4.82), I(4.75), I(3.7), I(0.85), [hs(ECGBOX[0]), ds(ECGBOX[1])])
    arrow_mid(f, [(I(6.67), I(ty + 2.3)), (I(6.67), I(4.75))])
    arrow_mid(f, [(I(4.3), I(ty + 2.3)), (I(4.3), I(5.17)), (I(4.82), I(5.17))])
    arrow_mid(f, [(I(10.7), I(ty + 2.3)), (I(10.7), I(5.17)), (I(8.52), I(5.17))])
    f.text(I(0.78), I(6.0), I(11.78), I(0.25), [FOOT(NOTE9)], name='Nota')
    f.text(I(0.78), I(6.3), I(11.78), I(0.25), [FOOT(LEG9)], name='Legenda')
    # ---- E2
    s = S[1]; f = frame(s)
    f.gbox('step', I(4.82), I(ty), I(3.7), I(0.8), [hs(ECGBOX[0]), ds(ECGBOX[1])])
    cxL, cxR = 2.63, 10.71
    arrow_mid(f, [(I(4.82), I(ty + 0.4)), (I(cxL), I(ty + 0.4)), (I(cxL), I(3.1))])
    arrow_mid(f, [(I(8.52), I(ty + 0.4)), (I(cxR), I(ty + 0.4)), (I(cxR), I(3.1))])
    f.gbox('step', I(0.78), I(3.1), I(3.7), I(0.9), [hs('> 1 ponto no ADD-RS ou com sinais sugestivos'), ds('no POCUS/Radiografia de tórax*')])
    f.gbox('step', I(8.86), I(3.1), I(3.7), I(0.9), [hs('≤ 1 ponto no ADD-RS e sem sinais sugestivos'), ds('no POCUS/Radiografia de tórax*')])
    arrow_mid(f, [(I(cxL), I(4.0)), (I(cxL), I(4.3))]); arrow_mid(f, [(I(cxR), I(4.0)), (I(cxR), I(4.3))])
    f.gbox('in', I(0.78), I(4.3), I(3.7), I(0.55), [sm('in', 'Alta probabilidade')])
    f.gbox('obs', I(8.86), I(4.3), I(3.7), I(0.55), [sm('obs', 'Baixa probabilidade')])
    arrow_mid(f, [(I(cxL), I(4.85)), (I(cxL), I(5.15))])
    f.gbox('step', I(0.78), I(5.15), I(3.7), I(0.8), [hs('Realizar angiotomografia de aorta torácica e abdominal')])
    f.text(I(0.78), I(6.05), I(11.78), I(0.25), [FOOT(NOTE9)], name='Nota')
    f.text(I(0.78), I(6.35), I(11.78), I(0.25), [FOOT(LEG9)], name='Legenda')
    # ---- E3
    s = S[2]; f = frame(s)
    f.gbox('obs', I(4.97), I(ty), I(3.4), I(0.6), [sm('obs', 'Baixa probabilidade')])
    arrow_mid(f, [(I(6.67), I(ty + 0.6)), (I(6.67), I(2.8))])
    f.gbox('step', I(4.97), I(2.8), I(3.4), I(0.6), [hs('D-Dímero')])
    arrow_mid(f, [(I(4.97), I(3.1)), (I(2.9), I(3.1)), (I(2.9), I(4.3))])
    arrow_mid(f, [(I(8.37), I(3.1)), (I(10.4), I(3.1)), (I(10.4), I(4.3))])
    f.label(I(3.0), I(3.15), '≥ 500 ng/ml', w=I(1.4))
    f.label(I(8.5), I(3.15), '<500 ng/ml', w=I(1.4))
    f.gbox('step', I(1.2), I(4.3), I(3.4), I(0.9), [hs('Realizar angiotomografia de aorta torácica e abdominal')])
    f.gbox('out', I(8.7), I(4.3), I(3.4), I(0.9), [sm('out', 'Rule-out para dissecção de aorta'), sm('out', 'Procurar outro diagnóstico')])
    f.text(I(0.78), I(6.3), I(11.78), I(0.25), [FOOT(LEG9)], name='Legenda')
    return S

# ---------------------------------------------------------------- FIGURA F (TEP – fig. 10)
ABREV = 'TEP: tromboembolismo pulmonar; PAS: pressão arterial sistólica; ECOTT: ecocardiograma transtorácico; VD: ventrículo direito; TC: angiotomografia computadorizada (protocolo TEP).'

def figF(prs, src):
    titles = ['Fluxograma TEP diagnóstico (%d/3)' % i for i in (1, 2, 3)]
    S = to_native_series(prs, src, titles)
    ty = 1.75
    # ---- F1
    s = S[0]; f = frame(s)
    f.gbox('pill', I(4.87), I(ty), I(3.6), I(0.6), [hp('SUSPEITA DE TEP')])
    arrow_mid(f, [(I(6.67), I(ty + 0.6)), (I(6.67), I(2.75))])
    f.diamond(I(4.77), I(2.75), I(3.8), I(1.5), ['CHOQUE OU', 'HIPOTENSÃO?'])
    cy = 3.5
    f.gbox('step', I(9.2), I(1.75), I(3.36), I(1.15), [ds('PAS ≤ 90 mmHg ou queda ≥ 40 mmHg por > 15’ não causada por arritmia aguda, sepse ou hipovolemia')], anchor='ctr')
    f.arrow([(I(9.2), I(2.32)), (I(8.72), I(2.32)), (I(8.72), I(3.35))], dash=True)
    arrow_mid(f, [(I(8.57), I(cy + 0.15)), (I(10.9), I(cy + 0.15)), (I(10.9), I(4.5))])
    f.label(I(8.65), I(cy + 0.15 - 0.28 + 0.36), 'Sim', w=I(0.45))
    f.gbox('in', I(9.4), I(4.5), I(3.0), I(0.8), [sm('in', 'ALTO RISCO', True, 15)])
    f.text(I(9.4), I(5.4), I(3.0), I(0.3), [plain('Acionar time de choque')], algn='ctr')
    arrow_mid(f, [(I(4.77), I(cy)), (I(2.9), I(cy)), (I(2.9), I(4.5))])
    f.label(I(4.15), I(cy - 0.28), 'Não', w=I(0.5), algn='r')
    f.gbox('out', I(0.9), I(4.5), I(4.0), I(0.8), [sm('out', 'CHECAR PROBABILIDADE DIAGNÓSTICA', True, 13)])
    f.text(I(0.9), I(5.4), I(4.0), I(0.3), [plain('Wells, Genebra, PERC')], algn='ctr')
    f.text(I(0.78), I(6.15), I(11.78), I(0.4), [FOOT(ABREV)], name='Legenda')
    # ---- F2
    s = S[1]; f = frame(s)
    f.gbox('in', I(3.2), I(ty), I(3.2), I(0.5), [sm('in', 'ALTO RISCO', True, 13)])
    arrow_mid(f, [(I(4.8), I(ty + 0.5)), (I(4.8), I(2.4))])
    f.diamond(I(2.7), I(2.4), I(4.2), I(1.4), ['ECOTT COM', 'SOBRECARGA', 'DE VD²?'])
    cy = 3.1
    f.gbox('step', I(8.6), I(2.65), I(3.96), I(0.9), [hs('Tratar a causa de instabilidade conforme avaliação clínica-ecocardiográfica'), ds('(exames adicionais de acordo com a suspeita diagnóstica)')])
    arrow_mid(f, [(I(6.9), I(cy)), (I(8.6), I(cy))]); f.label(I(6.95), I(cy - 0.28), 'Não', w=I(0.5))
    arrow_mid(f, [(I(4.8), I(3.8)), (I(4.8), I(4.1))]); f.label(I(4.9), I(3.82), 'Sim', w=I(0.45))
    f.gbox('step', I(3.6), I(4.1), I(2.4), I(0.45), [hs('Fazer TC')])
    f.arrow([(I(2.7), I(cy)), (I(1.6), I(cy)), (I(1.6), I(4.32)), (I(3.6), I(4.32))], dash=True)
    f.text(I(0.78), I(2.72), I(1.8), I(0.3), [plain('ECOTT indisponível')], name='Rótulo')
    arrow_mid(f, [(I(4.8), I(4.55)), (I(4.8), I(4.7)), (I(2.38), I(4.7)), (I(2.38), I(4.85))])
    arrow_mid(f, [(I(4.8), I(4.7)), (I(6.1), I(4.7)), (I(6.1), I(4.85))])
    f.gbox('step', I(0.78), I(4.85), I(3.2), I(1.1), [hs('TC negativa para TEP'), ds('Procurar outra causa de instabilidade')])
    f.gbox('step', I(4.5), I(4.85), I(3.2), I(1.1), [hs('TC positiva para TEP'), ds('Fibrinólise e/ou tratamento intervencionista (seguir diretrizes clínicas de TEP)')])
    f.arrow([(I(6.0), I(4.32)), (I(8.4), I(4.32)), (I(8.4), I(5.4)), (I(7.7), I(5.4))], dash=True)
    f.text(I(8.6), I(4.3), I(3.9), I(0.9), [plain('TC indisponível e/ou sem condições de transporte em paciente com sobrecarga de VD')], name='Rótulo')
    f.text(I(0.78), I(6.02), I(11.78), I(0.25), [FOOT('²Razão do diâmetro VD/VE ≥1.0; TAPSE <16 mm')], name='Nota')
    f.text(I(0.78), I(6.25), I(11.78), I(0.4), [FOOT(ABREV)], name='Legenda')
    # ---- F3
    s = S[2]; f = frame(s)
    f.gbox('out', I(4.87), I(1.8), I(3.6), I(0.6), [sm('out', 'CHECAR PROBABILIDADE DIAGNÓSTICA', True, 13)])
    f.text(I(1.2), I(1.9), I(3.5), I(0.3), [plain('Wells, Genebra, PERC')], algn='r')
    arrow_mid(f, [(I(6.67), I(2.4)), (I(6.67), I(2.55)), (I(2.8), I(2.55)), (I(2.8), I(2.75))])
    arrow_mid(f, [(I(6.67), I(2.55)), (I(10.6), I(2.55)), (I(10.6), I(2.75))])
    f.gbox('obs', I(1.2), I(2.75), I(3.2), I(0.7), [sm('obs', 'Baixa¹ ou Intermediária'), sm('obs', '(improvável)', False, 12)])
    f.gbox('in', I(9.0), I(2.75), I(3.2), I(0.7), [sm('in', 'Alta probabilidade'), sm('in', '(provável)', False, 12)])
    arrow_mid(f, [(I(2.8), I(3.45)), (I(2.8), I(3.65))])
    f.gbox('step', I(1.2), I(3.65), I(3.2), I(0.5), [hs('Fazer D-dímero')])
    arrow_mid(f, [(I(2.8), I(4.15)), (I(2.8), I(4.55))])
    f.label(I(2.9), I(4.2), 'Negativo³', w=I(1.0))
    f.gbox('out', I(1.2), I(4.55), I(3.2), I(0.55), [sm('out', 'Procurar outro diagnóstico')])
    arrow_mid(f, [(I(4.4), I(3.9)), (I(7.6), I(3.9)), (I(7.6), I(4.55))])
    f.label(I(4.5), I(3.62), 'Positivo³', w=I(1.0))
    f.gbox('step', I(6.4), I(4.55), I(2.4), I(0.55), [hs('TC')])
    arrow_mid(f, [(I(10.6), I(3.45)), (I(10.6), I(4.82)), (I(8.8), I(4.82))])
    f.text(I(0.78), I(5.25), I(11.78), I(0.9), [FOOT('¹Pacientes de baixa probabilidade clínica (Wells, Genebra) que não possuam nenhum critério do PERC presente são considerados de probabilidade muito baixa para o diagnóstico de TEP (em casos selecionados pode ser dispensável o D-dímero).'),
        FOOT('³D-dímero positivo ≥500 ng/mL (µg/L) ou, a partir dos usar 50 anos de idade, pode usar ponto de corte ajustado por idade (idade x 10) para melhor especificidade do ponto de corte do exame (abaixo do ponto de corte é D-dímero negativo).')], name='Nota')
    f.text(I(0.78), I(6.25), I(11.78), I(0.4), [FOOT(ABREV)], name='Legenda')
    return S

def run(prs, S):
    global TITLE_TEMPLATE
    TITLE_TEMPLATE = copy.deepcopy(title_el(S[28]))
    out = {}
    out[30] = figA(prs, S[29])
    out[31] = figA(prs, S[30])
    out[45] = figA(prs, S[44])
    out[33] = figB(prs, S[32])
    out[72] = figB(prs, S[71])
    out[43] = figC(prs, S[42])
    out[44] = figD(prs, S[43])
    out[50] = figE(prs, S[49])
    out[55] = figF(prs, S[54])
    return out
