from pathlib import Path
from argparse import ArgumentParser
from warnings import warn
import sys

from rplj.rplstuff.analyzer import BackupAnalyzer
from rplj.repoprep import init_repo
from rplj.jutils import prompt, free_path
import rplj.rplstuff.stalin as rstalin
import rplj.jmessages as jmessages
import rplj.jutils

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        '--repo',
        default='https://github.com/rplacelive/canvas1'
    )
    parser.add_argument('--repo-dir', type=Path)
    parser.add_argument('--since', '--after', dest='start')
    parser.add_argument('--until', '--before', dest='end')
    parser.add_argument('--output', default='out.png', type=Path)
    parser.add_argument('--force-overwrite', action='store_true')
    parser.add_argument('--force-clone', action='store_true')
    parser.add_argument('--force-pull', action='store_true')
    parser.add_argument(
        '--exclusion-list', 
        '--exclude',
        '--load-suspects',
        '--suspects',
        help='Skip analysis and perform clean up based on passed data.',
        dest='excluded'
    )
    parser.add_argument(
        '--heruistics-level',
        default='medium',
        choices=['low', 'medium', 'high']
    )
    parser.add_argument(
        '--clean-only',
        '--generate-template',
        action='store_true',
        dest='template'
    )
    parser.add_argument(
        '--dump-suspects',
        '--export-suspects',
        help='Dump suspect data to <file>, stdout or stderr.',
        dest='dump'
    )

    y_or_n = parser.add_mutually_exclusive_group()

    y_or_n.add_argument(
        '-y',
        action='store_true',
        help='Automatically answer positively to any prompt.'
    )
    y_or_n.add_argument(
        '-n',
        action='store_true',
        help='Automatically answer negatively to any prompt.'
    )

    return parser.parse_args()

def scan_commits(args, commits, overwrite_output):
    analyzer = BackupAnalyzer(args.heruistics_level)
    output, current_placers = analyzer.analyze(args, commits)

    if args.excluded:
        if not analyzer.parse_suspects(args.excluded):
            for splacer_id in args.excluded.replace(',', ' ').split():
                analyzer.suspects[int(splacer_id)].is_bot = True

    suspects = analyzer.suspects

    if args.dump:
        try:
            analyzer.dump_suspects(args.dump)
        except:
            warn(repr(sys.exception()))

    clean_pixels = rstalin.purge(args, commits, {
        i
        for i, placer_id in enumerate(current_placers)
        if (suspects[placer_id].is_bot
            or i in suspects[placer_id].botted_pixels)
        and i not in suspects[placer_id].clean_pixels
    }, suspects)

    if args.template:
        output.putpalette(
            np := bytes(output.getpalette('RGBA')) + b'\x00\x00\x00\x00',
            'RGBA'
        )
        output.putdata(
            (len(np) // 4 - 1).to_bytes()
            * output.width
            * output.height
        )

    for i, color in clean_pixels:
        output.putpixel((i % output.width, i // output.width), color)

    output.save(overwrite_output and args.output or free_path(args.output))

def main():
    args = parse_arguments()

    if args.excluded:
        if Path(args.excluded).is_file():
            args.excluded = Path(args.excluded).read_text()

    overwrite = False

    if args.output.exists():
        if (args.force_overwrite
                or prompt(jmessages.Q_OUTPUT_OVERWRITE(args.output))):
            overwrite = True

    rplj.jutils.AUTO_PROMPT = args.y or (not args.n and None)

    scan_commits(args, init_repo(args), overwrite)