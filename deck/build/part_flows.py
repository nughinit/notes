from lib import *
from flow import *

CX = 6097219          # centro da área útil
X0, X1 = 711403, 11483035
BH = E(0.66)          # altura padrão de pílula/etapa

def orig_notes(title, items):
    lines = ['TEXTO ORIGINAL DAS CAIXAS (antes de reduzir para 1–3 palavras) – %s' % title]
    for tag, txt in items:
        lines.append('• %s: %s' % (tag, txt))
    return '\n'.join(lines)

def move_text(slide, name, y, x=None, cx=None):
    for el in by_name(slide, name):
        set_geom(el, x=x, y=y, cx=cx)

# ------------------------------------------------------------------ slide 29
def slide29(prs, s):
    remove_flow_shapes(s, keep_names=('Mnemônico',))
    f = Flow(s)
    W, dW = E(3.4), E(3.0)
    y = E(1.5)
    f.pill(CX - W // 2, y, W, BH, ['Dor torácica instável'])
    y1 = y + BH; g = E(0.26)
    f.arrow([(CX, y1), (CX, y1 + g)])
    ys1 = y1 + g
    f.step(CX - W // 2, ys1, W, BH, ['Principais causas'])
    f.arrow([(CX, ys1 + BH), (CX, ys1 + BH + g)])
    ys2 = ys1 + BH + g
    f.step(CX - W // 2, ys2, W, BH, ['História, exame físico'])
    f.arrow([(CX, ys2 + BH), (CX, ys2 + BH + g)])
    yd = ys2 + BH + g; dH = E(1.3)
    f.diamond(CX - dW // 2, yd, dW, dH, ['Hipótese', 'definida?'])
    cy = yd + dH // 2
    RW = E(3.2); ry = E(5.78)
    lc, rc = CX - E(3.9), CX + E(3.9)
    f.pill(lc - RW // 2, ry, RW, BH, ['ECOCARDIOGRAMA'])
    f.pill(rc - RW // 2, ry, RW, BH, ['Seguir propedêutica'])
    f.arrow([(CX - dW // 2, cy), (lc, cy), (lc, ry)])
    f.arrow([(CX + dW // 2, cy), (rc, cy), (rc, ry)])
    f.label(CX - dW // 2 - E(0.62), cy - E(0.28), 'Não', w=E(0.52), algn='r')
    f.label(CX + dW // 2 + E(0.10), cy - E(0.28), 'Sim', w=E(0.52))
    set_notes(s, orig_notes('Dor torácica instável – Raciocínio diagnóstico', [
        ('Início', 'Paciente com dor torácica e instabilidade hemodinâmica'),
        ('Etapa 1', 'Pense nas principais causas'),
        ('Etapa 2', 'História e exame físico'),
        ('Decisão', 'Principal hipótese definida?'),
        ('Não', 'ECOCARDIOGRAMA'),
        ('Sim', 'Seguir a propedêutica da hipótese diagnóstica')]))
    return [s]

# ------------------------------------------------------------------ 59 / 77 / 61 (visão geral + detalhe)
def overview_detail(prs, s, cfg):
    """cfg: title, start, diamond(list), sim_step, nao_pill, rows [(step, end)], detail_label, notes, keep."""
    d = dup_slide(prs, s); move_after(prs, d, s)
    for sl in (s, d):
        remove_flow_shapes(sl, keep_names=cfg['keep'])
    set_title_suffix(s, ' (1/2)'); set_title_suffix(d, ' (2/2)')
    # --- visão geral
    f = Flow(s)
    BW = E(2.6); dW, dH = E(2.6), E(1.3); gap = E(0.6)
    yc = E(2.75)
    x = X0
    f.pill(x, yc - BH // 2, BW, BH, cfg['start'])
    xd = x + BW + gap
    f.arrow([(x + BW, yc), (xd, yc)])
    f.diamond(xd, yc - dH // 2, dW, dH, cfg['diamond'])
    xs = xd + dW + gap
    f.arrow([(xd + dW, yc), (xs, yc)])
    f.label(xd + dW + E(0.08), yc - E(0.30), 'Sim', w=E(0.45))
    f.step(xs, yc - BH // 2, BW, BH, cfg['sim_step'])
    y2 = E(4.5)
    f.pill(xs, y2 - BH // 2, BW, BH, cfg['nao_pill'])
    dcx = xd + dW // 2
    f.arrow([(dcx, yc + dH // 2), (dcx, y2), (xs, y2)])
    f.label(dcx + E(0.10), yc + dH // 2 + E(0.06), 'Não', w=E(0.5))
    # --- detalhe
    g = Flow(d)
    SW, PW = E(4.4), E(2.8); ag = E(0.7)
    xs0 = CX - (SW + ag + PW) // 2
    n = len(cfg['rows']); pitch = E(1.05)
    ytop = E(2.45) if n == 3 else E(2.7)
    g.label(xs0, E(1.7), cfg['detail_label'], w=E(6.0), color=APOIO, medium=False)
    for i, (st, en) in enumerate(cfg['rows']):
        yy = ytop + i * pitch
        g.step(xs0, yy - BH // 2, SW, BH, [st])
        g.pill(xs0 + SW + ag, yy - BH // 2, PW, BH, [en])
        g.arrow([(xs0 + SW, yy), (xs0 + SW + ag, yy)])
    # nota / legenda
    for sl in (s, d):
        move_text(sl, 'Nota', E(5.3), x=X0, cx=X1 - X0)
        move_text(sl, 'Legenda', E(5.72), x=X0, cx=X1 - X0)
    set_notes(s, cfg['notes'])
    set_notes(d, cfg['notes'])
    return [s, d]

def slide59(prs, s, keep=('Nota', 'Legenda')):
    cfg = dict(start=['Sem DAC conhecida'], diamond=['Teste prévio?'], sim_step=['Resultado do teste'],
               nao_pill=['Angio-TC ou estresse*'], keep=keep,
               rows=[('Negativo e recente', 'Considerar Alta'),
                     ('Estresse inconclusivo', 'Angio-TC'),
                     ('Isquemia moderada/importante', 'CATE')],
               detail_label='Teste prévio: Sim',
               notes=orig_notes('Investigação não invasiva – Sem DAC conhecida', [
                   ('Início', 'Sem doença arterial coronariana conhecida'),
                   ('Decisão', 'Teste prévio?'),
                   ('Sim → resultado (slide de detalhe)', 'caixa de resumo “Resultado do teste” criada na divisão do fluxo (não existia no original)'),
                   ('Sim, etapa 1', 'Negativo e recente → Considerar Alta'),
                   ('Sim, etapa 2', 'Teste de estresse inconclusivo ou anormalidade discreta → Angio-TC'),
                   ('Sim, etapa 3', 'Teste de estresse com isquemia moderada a importante / Sem CATE prévio → CATE'),
                   ('Não', 'Angio-TC ou teste de estresse*'),
                   ('Nota', '*Escolha do teste deve ser guiada pela disponibilidade e expertise.')]))
    return overview_detail(prs, s, cfg)

def slide61(prs, s):
    cfg = dict(start=['DAC conhecida'], diamond=['Obstrutiva?'], sim_step=['Critérios de risco'],
               nao_pill=['Angio-TC (preferência)*'], keep=('Nota', 'Legenda'),
               rows=[('Alto risco', 'CATE'), ('Sem alto risco', 'Estresse (preferência)*')],
               detail_label='Obstrutiva: Sim',
               notes=orig_notes('Investigação não invasiva – DAC conhecida', [
                   ('Início', 'DAC conhecida'),
                   ('Decisão', 'Obstrutiva?'),
                   ('Sim → critérios (slide de detalhe)', 'caixa de resumo “Critérios de risco” criada na divisão do fluxo (não existia no original)'),
                   ('Sim, etapa 1', 'Critérios de alto risco → CATE'),
                   ('Sim, etapa 2', 'Sem critérios de alto risco → Teste de estresse (preferência)*'),
                   ('Não', 'Angio-TC (preferência)*'),
                   ('Nota', '*Escolha do teste deve ser guiada pela disponibilidade e expertise.')]))
    return overview_detail(prs, s, cfg)

# ------------------------------------------------------------------ slide 63
def slide63(prs, s):
    d = dup_slide(prs, s); move_after(prs, d, s)
    for sl in (s, d):
        remove_flow_shapes(sl, keep_names=('Legenda',))
    set_title_suffix(s, ' (1/2)'); set_title_suffix(d, ' (2/2)')
    W = E(3.4)
    # (1/2)
    f = Flow(s)
    y = E(1.6)
    f.pill(CX - W // 2, y, W, BH, ['Troponina elevada'])
    g = E(0.6)
    f.arrow([(CX, y + BH), (CX, y + BH + g)])
    y2 = y + BH + g
    f.step(CX - W // 2, y2, W, BH, ['Excluir alternativos'])
    ymid = y2 + BH + E(0.42); y3 = y2 + BH + E(0.85)
    lc, rc = CX - E(2.1), CX + E(2.1)
    f.step(lc - W // 2, y3, W, BH, ['Rever angiografia'])
    f.step(rc - W // 2, y3, W, BH, ['Rever função VE'])
    f.arrow([(CX, y2 + BH), (CX, ymid), (lc, ymid), (lc, y3)])
    f.arrow([(CX, y2 + BH), (CX, ymid), (rc, ymid), (rc, y3)])
    f.label(CX + E(0.14), y2 + BH + E(0.08), 'Primeira etapa', w=E(1.5))
    # (2/2)
    h = Flow(d)
    y = E(1.6)
    h.pill(CX - W // 2, y, W, BH, ['Segunda etapa'])
    SW = E(3.2); ymid = y + BH + E(0.42); y3 = y + BH + E(0.85)
    cs = [CX - E(3.9), CX, CX + E(3.9)]
    for c, t in zip(cs, ['RM cardíaca', 'IVUS e OCT', 'Testes provocativos']):
        h.step(c - SW // 2, y3, SW, BH, [t])
        h.arrow([(CX, y + BH), (CX, ymid), (c, ymid), (c, y3)])
    for sl in (s, d):
        move_text(sl, 'Legenda', E(5.5), x=X0, cx=X1 - X0)
    n1 = orig_notes('Diagnóstico – IAM com coronariografia normal (1/2)', [
        ('Início', 'Elevação de troponina + Angiografia normal ou lesão < 50%'),
        ('Etapa', 'Excluir diagnósticos alternativos: - Sepse - TEP - Contusão cardíaca - Outras causas de elevação de troponina não cardiológica'),
        ('Primeira etapa, caixa 1', 'Rever achados da angiografia: DAC; Dissecção coronariana; Embolia e trombo coronariano'),
        ('Primeira etapa, caixa 2', 'Rever função do VE (Eco e ventriculografia): Takotsubo; Outras cardiomiopatias')])
    n2 = orig_notes('Diagnóstico – IAM com coronariografia normal (2/2)', [
        ('Segunda etapa, caixa 1', 'RM cardíaca: DAC; Miocardite; Outras cardiomiopatias'),
        ('Segunda etapa, caixa 2', 'Imagem vascular intracoronariana (IVUS e OCT): Ruptura de placa; Embolia e trombo coronariano; Dissecção coronariana'),
        ('Segunda etapa, caixa 3', 'Testes provocativos e funcionais: Espasmo coronariano; Doença microvascular')])
    set_notes(s, n1); set_notes(d, n2)
    return [s, d]

# ------------------------------------------------------------------ slide 73
def slide73(prs, s):
    remove_flow_shapes(s, keep_names=('Figura', 'Definição'))
    f = Flow(s)
    dcx = E(8.42)
    dW, dH = E(4.7), E(1.75)
    yd = E(3.17)
    f.arrow([(dcx, E(2.87)), (dcx, yd)])
    f.diamond(dcx - dW // 2, yd, dW, dH, ['Suspeita de SCA', 'ou Síndromes Aórticas', 'Agudas ou TEP?'])
    cy = yd + dH // 2
    PW = E(3.3); py = E(5.72)
    lc, rc = E(5.36), E(10.86)
    f.pill(lc - PW // 2, py, PW, BH, ['Propedêutica Específica'])
    f.pill(rc - PW // 2, py, PW, BH, ['Escores de risco'])
    f.arrow([(dcx - dW // 2, cy), (lc, cy), (lc, py)])
    f.arrow([(dcx + dW // 2, cy), (rc, cy), (rc, py)])
    f.label(dcx - dW // 2 - E(0.55), cy - E(0.28), 'Não', w=E(0.5), algn='r')
    f.label(dcx + dW // 2 + E(0.06), cy - E(0.28), 'Sim', w=E(0.5))
    set_notes(s, orig_notes('Paciente sem critérios de instabilidade', [
        ('Decisão', 'Suspeita de SCA ou Síndromes Aórticas Agudas ou TEP ?'),
        ('Não', 'Propedêutica Específica'),
        ('Sim', 'Escores Clínicos de Risco e Probabilidade Diagnóstica')]))
    return [s]

def run(prs, S):
    out = {}
    out[29] = slide29(prs, S[28])
    out[59] = slide59(prs, S[58])
    out[61] = slide61(prs, S[60])
    out[63] = slide63(prs, S[62])
    out[73] = slide73(prs, S[72])
    out[77] = slide59(prs, S[76], keep=('Nota',))
    return out
