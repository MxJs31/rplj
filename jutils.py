from pathlib import Path

AUTO_PROMPT = None

def prompt(message, yes='y', no='n', *, force=False):
    if AUTO_PROMPT is not None and not force:
        return bool(AUTO_PROMPT)

    while (result := input(f'{message} ({yes} / {no}) ')) not in (yes, no):
        print(f'Write either \"{yes}\" or \"{no}\"...', end=' ')

    return result == yes

def free_path(path):
    path = Path(path) # lol

    if not path.exists():
        return path

    orig_stem = path.stem
    i = 0

    while (result_path := path.with_stem(orig_stem + str(i))).exists():
        i += 1

    return result_path