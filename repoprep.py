from shutil import which
from pathlib import Path
from urllib.parse import urlparse
from subprocess import run

from rplj.jutils import prompt
import rplj.jmessages as jmessages

def init_repo(args):
    if not which('git'):
        raise FileNotFoundError(jmessages.NO_GIT)

    if not args.repo_dir:
        args.repo_dir = Path(Path(urlparse(args.repo).path).stem)

    if (args.repo_dir / '.git').is_dir():
        if not ((args.repo_dir / 'place').is_file()
                and (args.repo_dir / 'placers').is_file()):
            raise Exception(jmessages.INCOMPATIBLE_REPO)

        if args.force_pull or prompt(jmessages.Q_UPDATE):
            run(['git', 'pull'], cwd=args.repo_dir, check=True)
    else:
        if (not args.force_clone
                and not prompt(jmessages.Q_CLONE(args.repo_dir, args.repo))):
            raise Exception(jmessages.NO_CLONE)

        run(['git', 'clone', args.repo, args.repo_dir], check=True)

    commits = [
        (hash, int(ts))
        for hash, ts in [combined.split(',') for combined in run(
            ['git', 'log']
            + (args.start and [f'--since=\"{args.start}\"'] or [])
            + (args.end and [f'--until=\"{args.end}\"'] or [])
            + ['--pretty=tformat:%H,%ct'],
            cwd=args.repo_dir,
            capture_output=True,
            check=True,
            text=True
        ).stdout.split()]
    ]

    if not commits:
        raise Exception(jmessages.NO_COMMITS)

    return commits