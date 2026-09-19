from subprocess import run
from io import BytesIO
from zipfile import ZipFile
from warnings import warn
import sys

from rplj.rplstuff.analyzer import BackupAnalyzer

def purge(args, commits, dirty_pixels, suspects):
    clean_pixels = set()

    try:
        for commit_hash, commit_ts in commits:
            if len(dirty_pixels) == 0:
                break

            canvas, placers = BackupAnalyzer.extract_data(
                commit_hash,
                args.repo_dir
            )

            canvas_bytes = canvas.tobytes()
            deferred_remove = set()

            for i in dirty_pixels:
                if (i in suspects[placers[i]].clean_pixels
                    or (not suspects[placers[i]].is_bot
                        and i not in suspects[placers[i]].botted_pixels)):
                    clean_pixels.add((i, canvas_bytes[i]))
                    deferred_remove.add(i)

            dirty_pixels -= deferred_remove
            deferred_remove.clear()
    except:
        warn(repr(sys.exception()))

    return clean_pixels