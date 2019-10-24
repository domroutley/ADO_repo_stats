# Azure DevOps repository statistics python module

*It is strongly suggested that you use a virtual python environment.  
Install:`python3 -m venv .venv`  
Run:`source .venv/bin/activate`  
Test:`which python3`  
(should give path to .venv/bin/python3, not global python location)  
Stop:`deactivate`*

## To run
- Clone repo  
  `git clone https://github.com/domroutley/ADO_repo_stats.git`
- Install required packages  
  `pip install -r requirements.txt`
- Change the organisation and project variables in the `target.py` file
- Create a `token` file in the same directory and put your PAT for the target project in it
- Run the `main.py` file (using python 3)


## What this code does
- Outputs 5 .csv files
  - [project name]/[project name]-overview.csv
  - [project name]/project name]-git.csv
  - [project name]/project name]-build.csv
  - [project name]/project name]-release.csv

### Overview file contains...
- [x] Number of repositories
- [x] Number of commits in total
- [x] Number of builds
- [x] Number of build definitions
- [ ] Average time per build
- [x] Number of releases
- [x] Number of release definitions
- [ ] Average time per release deployment

### Git file contains...
- [x] Number of repositories
- [x] Default branch of repository
- [x] Number of commits in total (for project)
- [x] Number of commits per repo
- [ ] Number of commits not in master (per repo)
- [ ] Number of lines in master per repo (unknown)

### Build file contains...
- [x] Number of builds
- [x] Number of build definitions
- [x] Number of builds per definition
- [x] Number of each type of outcome for a build per definition
- [ ] Time per build (print build ids)
- [ ] Average time per build

### Release file contains...
- [x] Number of release deployments
- [x] Number of release definitions
- [x] Number of deployments per definition
- [x] Number of each type of outcome for a deployment per definition
- [ ] Time per deployment (print deployment ids)
- [ ] Average time per deployment

#TODO
- [ ] Rewrite all calls to the API to use direct calls
