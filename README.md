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
  - [project name]/project name]-all.csv

### Overview file contains...
- [x] Number of repositories
- [ ] ~~Number of commits in total~~ (on hold for API update)
- [x] Number of builds
- [ ] Number of build definitions
- [ ] Average time per build
- [x] Number of releases
- [ ] Number of release definitions
- [ ] Average time per release

### Git file contains...
- [x] Number of repositories
- [x] Default branch of repository
- [ ] ~~Number of commits in total (for project)~~ (on hold for API update)
- [ ] ~~Number of commits per repo~~ (on hold for API update)
- [ ] ~~Number of lines in master per repo~~ (unknown how to do)

### Build file contains...
- [x] Number of builds
- [ ] Number of build definitions
- [x] Number of builds per definition
- [x] Number of successful builds per definition
- [x] Number of failed builds per definition
- [x] Number of cancelled builds per definition
- [ ] Time per build
- [ ] Average time per build

### Release file contains...
For each release:
- [x] Release definition
- [ ] Number of deployments and their status (sort by release definition)
- [ ] What environment release was made into

### All file contains...
- Everything that the other files do, in one big long list

#TODO
- Rewrite all calls to the API to use direct calls
