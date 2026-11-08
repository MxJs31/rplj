"""
    Detect behavior patterns only found in multi-botting
    or multi-accounting. 
"""

from math import isclose
from collections import defaultdict

def init(analyzer):
    pass

def scan(analyzer):
    if not analyzer.data.prev:
        return

    top_placed = sorted(
        {
            placer_id: len(
                analyzer.data.prev.placers.get_placer_pixels()
                - analyzer.data.cur.placers.get_placer_pixels()
            )
            for placer_id in set(analyzer.data.cur.placers)
        }.items(),
        key=lambda entry: entry[1],
        reverse=True
    )
    similar = defaultdict(list)
    locked_i = 0

    for i in range(1, len(top_placed)):
        if isclose(
            top_placed[i][1],
            top_placed[locked_i][1],
            rel_tol=analyzer.rel_tol / 2
        ):
            similar[top_placed[locked_i][0]].append((top_placed[i][0]))
        else:
            locked_i = i