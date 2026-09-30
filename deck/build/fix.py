import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import part_tables, part_flows, part_charts, part_g

SRC = '/home/user/notes/deck/original.pptx'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/notes/deck/work.pptx'

prs = Presentation(SRC)
S = list(prs.slides)
series = {}
series.update(part_tables.run(prs, S))
series.update(part_flows.run(prs, S))
series.update(part_charts.run(prs, S))
series.update(part_g.run(prs, S))
renumber_footers(prs)
prs.save(OUT)
print('slides:', len(prs.slides))

import json
pos = {}
allslides = list(prs.slides)
def position(sl):
    for i, x in enumerate(allslides, 1):
        if x._element is sl._element: return i
for n, lst in series.items():
    pos[n] = [position(s) for s in lst]
json.dump(pos, open('/home/user/notes/deck/build/positions.json', 'w'), indent=1)
print(pos)
