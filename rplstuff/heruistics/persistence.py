"""
    Detect one of the most common and obvious automation
    patterns: unnatural persistence.
"""

from math import isclose
from statistics import fmean

max_pps = 0
active_placers_prev = 0
intolerable_unemployment = None

def init(analyzer):
    global intolerable_unemployment

    intolerable_unemployment = {
        'low': 2.5,
        'medium': 1.5,
        'high': 1
    }[analyzer.heruistics_level]

def scan(analyzer):
    if not analyzer.data.prev:
        return

    global max_pps
    global active_placers_prev

    max_pps_commit = 0
    active_placers = 0
    trial_list = []

    for placer_id in set(analyzer.data.cur.placers):
        if not hasattr(analyzer.suspects[placer_id], 'activity'):
            analyzer.suspects[placer_id].activity = []

        activity = analyzer.suspects[placer_id].activity
        dt = analyzer.data.prev.commit_ts - analyzer.data.cur.commit_ts
        placed_pixels = (
            analyzer.data.prev.placers.get_placer_pixels(placer_id)
            - analyzer.data.cur.placers.get_placer_pixels(placer_id)
        )
        pps = len(placed_pixels) / dt

        if pps > 0:
            active_placers += 1

            activity.insert(0, (pps, placed_pixels, dt))
        elif len(activity):
            trial_list.append(placer_id)

        if pps > max_pps_commit:
            max_pps_commit = pps

    max_pps = (
        max_pps_commit if max_pps_commit >= max_pps
        else fmean(
            (max_pps_commit, max_pps),
            (active_placers, active_placers_prev)
        )
    )
    active_placers_prev = active_placers

    for placer_id in trial_list:
        activity = analyzer.suspects[placer_id].activity
        m = fmean([
            a[0]
            for a in (len(activity) > 2 and activity[1 : -1] or activity)
        ])
        uh = sum([
            a[2] / (
                isclose(a[0], max_pps, rel_tol=analyzer.rel_tol)
                and not isclose(a[0], m, rel_tol=analyzer.rel_tol)
                and 2
                or 1
            )
            for a in activity
            if isclose(a[0], m, rel_tol=analyzer.rel_tol)
                or isclose(a[0], max_pps, rel_tol=analyzer.rel_tol)
        ]) / 3600

        if (uh > intolerable_unemployment
                or isclose(
                    uh,
                    intolerable_unemployment,
                    rel_tol=analyzer.rel_tol
                )):
            analyzer.suspects[placer_id].traits['unemployed'] += (
                0.6 * uh
                / intolerable_unemployment
            )
        else:
            analyzer.suspects[placer_id].clean_pixels.update(*[
                a[1]
                for a in activity
            ])

        activity.clear()
