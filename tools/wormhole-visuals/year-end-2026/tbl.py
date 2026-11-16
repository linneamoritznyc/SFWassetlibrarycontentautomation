def table(x,y,w,widths,rows,styles,rc,pad=(12,14)):
    # rows: list of tuples of cell text; styles: per-column css (font etc.)
    h=f'<table style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-collapse:collapse;table-layout:fixed"><colgroup>'+''.join(f'<col style="width:{cw}px">' for cw in widths)+'</colgroup>'
    for r in rows:
        h+='<tr>'+''.join(f'<td style="vertical-align:top;padding:{pad[0]}px {pad[1] if j<len(r)-1 else 0}px {pad[0]}px 0;border-bottom:1px solid {rc};{c[1] if isinstance(c,tuple) else styles[j]}">{c[0] if isinstance(c,tuple) else c}</td>' for j,c in enumerate(r))+'</tr>'
    return h+'</table>'
