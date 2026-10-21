from array import array
from functools import cached_property
from collections import defaultdict
import sys

class Placers(array):
    if sys.byteorder == 'little':
        def __new__(cls, placers):
            (obj := super().__new__(cls, 'I', placers)).byteswap()

            return obj
    else:
        def __new__(cls, placers):
            return super().__new__(cls, 'I', placers)

    @cached_property
    def as_dict(self):
        dct = defaultdict(set)

        for i, placer_id in enumerate(self):
            dct[placer_id].add(i)

        return dct

    def get_top_placers(self):
        top_placers = {}

        for placer_id in self:
            if placer_id not in top_placers:
                top_placers[placer_id] = 0

            top_placers[placer_id] += 1

        return sorted(
            top_placers.items(),
            key=lambda entry: entry[1],
            reverse=True
        )

    def get_placer_pixels(self, target_placer_id):
        return self.as_dict[target_placer_id]

    def get_placer_pixel_count(self, target_placer_id):
        return self.count(target_placer_id)