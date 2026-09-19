NO_GIT = 'Git must be installed and added to path'
NO_CLONE = 'cannot clone into the specified directory'
NO_COMMITS = 'empty commit log'
INCOMPATIBLE_REPO = 'the specified directory contains an incompatible Git repo'
Q_UPDATE = 'The repo might be outdated, update via \"git pull\"?'
Q_OUTPUT_OVERWRITE = lambda output: f'The specified output file ({output}) \
already exists, overwrite?'
Q_CLONE = lambda repo_dir, repo: f'The specified directory ({repo_dir}) \
{repo_dir.is_dir() and 'is not a Git repo' or 'does not exist'}, clone repo \
({repo}) into it (might take a significant amount of time and traffic)?'