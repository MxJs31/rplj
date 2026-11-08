from pathlib import Path

AUTO_PROMPT = None
HIDE_PROGRESS = False
ANIM_PROGRESS = 0
ANIM_CHAR_SET = r"\|/-"

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

def progress(message='', done=None, total=None, anim_only=False):
    global ANIM_PROGRESS

    if HIDE_PROGRESS:
        return

    result = [(
        ANIM_CHAR_SET[ANIM_PROGRESS] if done is None or done != total
        else 'V'
    )]

    if not anim_only:
        if message:
            result.append(message)

        result.append(f'({done} / {total})')

    print(' '.join(result), end=(
        '\r' if done is None or done != total
        else '\n'
    ))

    ANIM_PROGRESS += 1

    if not (0 <= ANIM_PROGRESS < len(ANIM_CHAR_SET)):
        ANIM_PROGRESS = 0