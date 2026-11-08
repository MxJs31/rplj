from json import dump, loads
from types import SimpleNamespace
from sys import stdout, stderr
from zipfile import ZipFile
from io import BytesIO
from subprocess import run
from warnings import warn
from time import time
from math import isclose
from collections import defaultdict
import sys

from PIL import Image

from rplj.rplstuff.placers import Placers
from rplj.rplstuff.heruistics import analyzers
from rplj.jutils import free_path, progress

class Suspect(SimpleNamespace):
    def __init__(self, *args, **kwargs):
        self.traits = defaultdict(float)
        self.botted_pixels = set()
        self.clean_pixels = set()

        super().__init__(*args, **kwargs)

    def bot_score(self):
        return min(1, max(0, sum(self.traits.values())))

class Suspects(dict):
    def __missing__(self, key):
        self[key] = Suspect()

        return self[key]

class BackupAnalyzer:
    def __init__(self, heruistics_level='medium'):
        self.rel_tol = {
            'low': 0.2,
            'medium': 0.27,
            'high': 0.33
        }[heruistics_level]
        self.heruistics_level = heruistics_level
        self.suspects = Suspects()
        self.data = SimpleNamespace(
            cur=None,
            prev=None
        )

        for analyzer in analyzers.values():
            analyzer.init(self)

    def analyze(self, args, commits):
        output = None
        current_placers = None
        len_commits = len(commits)
        progress_ts = 0

        try:
            for i in range(len_commits):
                commit_hash, commit_ts = commits[i]
                canvas, placers = self.extract_data(commit_hash, args.repo_dir)

                if output is None:
                    output = canvas.copy()
                    current_placers = placers

                    if args.excluded:
                        break

                if time() - progress_ts >= 1:
                    progress('analyzing backups', i, len_commits)

                    progress_ts = time()

                self.feed(commit_ts=commit_ts, canvas=canvas, placers=placers)

                # to-do:
                # 1. make a more accurate set of checks;
                # 2. perform expensive checks only for backups that are distant
                #    from the latest
                if set(current_placers).isdisjoint(set(placers)):
                    break
        except:
            warn(repr(sys.exception()))

        return output, current_placers

    def feed(self, *, commit_ts, canvas, placers):
        self.data.cur = SimpleNamespace(
            commit_ts=commit_ts,
            canvas=canvas,
            placers=placers
        )

        for analyzer in analyzers.values():
            analyzer.scan(self)

        self.data.prev = self.data.cur

    def dump_suspects(self, where):
        dump(
            self.suspects,
            where.lower() in ('stdout', 'stderr') and {
                'stdout': stdout,
                'stderr': stderr
            }[where.lower()] or free_path(where).open('w'),
            default=lambda obj: (
                obj.__dict__ if isinstance(obj, SimpleNamespace)
                else list(obj)
            )
        )

    def parse_suspects(self, suspects_dump):
        try:
            suspects = loads(suspects_dump)
        except:
            return False

        if not isinstance(suspects, dict):
            return False

        suspects = Suspects({
            int(placer_id): Suspect(**suspect)
            for placer_id, suspect in suspects.items()
        })

        for suspect in suspects:
            suspect.botted_pixels = set(suspect.botted_pixels)
            suspect.clean_pixels = set(suspect.clean_pixels)

        self.suspects = suspects

        return True

    def is_bot(self, placer_id):
        return isclose(
            self.suspects[placer_id].bot_score(),
            1,
            rel_tol=self.rel_tol
        )

    @staticmethod
    def extract_data(commit_hash, repo_dir):
        backup = ZipFile(BytesIO(run(
            ['git', 'archive', '--format=zip', '-0', commit_hash],
            cwd=repo_dir,
            capture_output=True,
            check=True
        ).stdout))
        placers = Placers(backup.read('placers'))
        metadata = loads(backup.read('metadata.json'))

        (canvas := Image.frombytes(
            'P',
            (metadata['width'], metadata['height']),
            backup.read('place')
        )).putpalette(b''.join([
            color.to_bytes(4)
            for color in metadata['palette']
        ]), 'RGBA')

        return canvas, placers