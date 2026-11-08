# rplace.live janitor
Generate full canvas images or clean-up templates free of botted content.
## Running
rplace.live janitor is a Python module that can be executed using the `-m` switch:
`python -m rplj`

Note: the `-m` switch requires a module name to be passed as its argument, so the directory containing the module must be either located in the current working directory of the command prompt or installed as a Python module.
## Command line switches
To get all the supported command line switches, run this module with the `-h` switch:
`python -m rplj -h`

It should print the following:
```
usage: __main__.py [-h] [--repo REPO] [--repo-dir REPO_DIR] [--since START] [--until END] [--output OUTPUT]
                   [--force-overwrite] [--force-clone] [--force-pull] [--exclusion-list EXCLUDED]
                   [--heruistics-level {low,medium,high}] [--clean-only] [--dump-suspects DUMP] [--hide-progress]
                   [-y | -n]

options:
  -h, --help            show this help message and exit
  --repo REPO
  --repo-dir REPO_DIR
  --since START, --after START
  --until END, --before END
  --output OUTPUT
  --force-overwrite
  --force-clone
  --force-pull
  --exclusion-list EXCLUDED, --exclude EXCLUDED, --load-suspects EXCLUDED, --suspects EXCLUDED
                        Skip analysis and perform clean up based on passed data.
  --heruistics-level {low,medium,high}
  --clean-only, --generate-template
  --dump-suspects DUMP, --export-suspects DUMP
                        Dump suspect data to <file>, stdout or stderr.
  --hide-progress
  -y                    Automatically answer positively to any prompt.
  -n                    Automatically answer negatively to any prompt.
```
Where:
* Switches in square brackets are optional;
* The pipe symbol `|` denotes mutually exclusive switches; 
* Aliases for some switches are separated by commas;
* Curly brackets contain all the possible values for switches that take a limited set of options.
