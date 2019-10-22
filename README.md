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
- [ ] Number of repositories
- [ ] Number of commits in total
- [ ] Number of branches created
- [ ] Number of builds
- [ ] Number of build definitions
- [ ] Average time per build
- [ ] Number of releases
- [ ] Number of release definitions
- [ ] Average time per release

### Git file contains...
- [ ] Number of repositories
- [ ] Number of commits in total
- [ ] Number of branches created
- [ ] Number of commits per repo
- [ ] Number of branches created per repo
- [ ] Number of lines in master per repo

### Build file contains...
- [ ] Number of builds
- [ ] Number of build definitions
- [ ] Number of builds per definition
- [ ] Number of successful builds per definition
- [ ] Number of failed builds per definition
- [ ] Number of cancelled builds per definition
- [ ] Time per build
- [ ] Average time per build

### Release file contains...
For each release:
- [ ] Release definition
- [ ] Number of deployments and their status (sort by release definition)
- [ ] What environment release was made into

### All file contains...
- Everything that the other files do, in one big long list
