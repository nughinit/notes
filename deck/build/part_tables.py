from lib import *

FULL_W = 10771632
BOTTOM_MAX = 6100000

# (slide, [ partes ]) ; cada parte: dict(keep=[ids extras], rows={id:[linhas]}, ...)
def run(prs, S):
    """S: lista dos slides originais (índice 0 = slide 1). Retorna {n: [slides da série]}."""
    out = {}

    def series(n, parts, font13=False, widen=(), legend_of=None):
        src = S[n - 1]
        slides = [src] + [dup_slide(prs, src) for _ in parts[1:]]
        ref = src
        for s in slides[1:]:
            move_after(prs, s, ref); ref = s
        N = len(parts)
        for k, (s, part) in enumerate(zip(slides, parts), 1):
            keep_only(s, part['keep'])
            for sid, rows in part.get('rows', {}).items():
                gf = shape_by_id(s, sid)
                keep_rows(table_of(gf), set(rows))
            if N > 1:
                set_title_suffix(s, ' (%d/%d)' % (k, N))
            for sid in part.get('font13', []):
                set_table_font(table_of(shape_by_id(s, sid)), 13)
            for sid in part.get('widen', []):
                scale_table_width(shape_by_id(s, sid), FULL_W)
            part['layout'](s, part) if 'layout' in part else None
        out[n] = slides
        return slides

    def stack(s, part):
        """table (+ legenda opcional acima) (+ nota abaixo) a partir do topo."""
        nl = title_lines(s)
        y = part.get('y0') or {1: 1417320, 2: 1640000}.get(nl, 2150000)
        if part.get('legend'):
            lg = shape_by_id(s, part['legend'])
            set_geom(lg, x=711403, y=y, cx=FULL_W if part.get('legend_full', True) else None)
            y += 238308
        gf = shape_by_id(s, part['table'])
        set_geom(gf, x=711403, y=y)
        h = fit_table(gf)
        y += h
        for nid in part.get('notes', []):
            nt = shape_by_id(s, nid)
            set_geom(nt, x=711403, y=y + 70000, cx=FULL_W)
            y += 70000 + geom(nt)[3] + 20000
        assert y <= BOTTOM_MAX, (title_text(s), y)
        part['_bottom'] = y

    # ---- slide 14 ---------------------------------------------------------
    def lay14(s, part):
        gf = shape_by_id(s, 1030)
        set_geom(gf, y=1417320)
        h = fit_table(gf)
        assert 1417320 + h <= BOTTOM_MAX, h
    r14 = lambda rows: dict(keep=[1030, 1031], rows={1030: rows}, font13=[1030], layout=lay14)
    series(14, [r14(list(range(0, 7))), r14([0] + list(range(7, 13))), r14([0] + list(range(13, 18)))])

    # ---- 1 tabela + nota, sem mudar fonte (já 13) ---------------------------
    def simple(n, rowsets, table=6, nota=7):
        parts = [dict(keep=[table, nota], rows={table: r}, table=table, notes=[nota], layout=stack) for r in rowsets]
        series(n, parts)
    simple(51, [[0, 1, 2, 3, 4], [0, 5, 6, 7]])
    simple(52, [[0, 1, 2, 3, 4], [5, 6, 7, 8]])
    simple(54, [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]])
    simple(65, [list(range(0, 6)), [0] + list(range(6, 10))])
    simple(66, [[0, 1, 2, 3, 4], [0, 5, 6, 7]])
    simple(71, [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]])

    # ---- slide 53 -----------------------------------------------------------
    def p53(table, rows):
        return dict(keep=[6, table, 10], rows={table: rows}, table=table, notes=[10], font13=[table], widen=[table], y0=1640000, layout=stack)
    series(53, [p53(7, list(range(0, 6))), p53(7, [0] + list(range(6, 10))), p53(8, [0, 1, 2, 3]), p53(9, [0, 1, 2, 3])])

    # ---- slide 74 -----------------------------------------------------------
    def lay74a(s, part):
        y = 1417320
        set_geom(shape_by_id(s, 6), y=y); y += 238308
        gf = shape_by_id(s, 7); set_geom(gf, y=y); h = fit_table(gf)
        box = shape_by_id(s, 8); set_geom(box, y=y, cy=h)
        assert y + h <= BOTTOM_MAX
    p74a = dict(keep=[6, 7, 8], font13=[7], layout=lay74a)
    p74b = dict(keep=[9, 10, 11], font13=[10], table=10, legend=9, notes=[11], layout=stack)
    series(74, [p74a, p74b])

    # ---- slide 75 -----------------------------------------------------------
    def p75(legend, table, rows, notes, widen=True):
        return dict(keep=[legend, table] + notes, rows={table: rows}, table=table, legend=legend, notes=notes,
                    font13=[table], widen=[table] if widen else [], layout=stack)
    series(75, [p75(6, 7, [0, 1, 2, 3, 4], [10]), p75(6, 7, [0, 5, 6, 7], [10]),
                p75(8, 9, [0, 1, 2, 3, 4], [10]), p75(8, 9, [5, 6, 7, 8], [10]),
                p75(11, 12, [0, 1, 2], [13], widen=False)])
    return out
