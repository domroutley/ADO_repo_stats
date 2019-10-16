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
- Using either a python script, or in the interpreter...
  - Import the Project class  
    `from ADOStats import Project`
  - Initialise the project  
    `myProject = Project([ORGANISATION],[PROJECT],[PERSONAL_ACCESS_TOKEN])`
- Alternativly, use the `exampleUsage.py` file to just run the module. You will need to create a `token` file containing only a PAT for ADO, and change the project initialisation call to use your organisation and project names.


## Targets
- [x] Number of repositories


- [x] Number of builds
- [x] Number of build definitions
- [x] Number of builds per definition
- [x] Number of successful builds per definition
- [x] Number of failed builds per definition
- [x] Number of cancelled builds per definition


- [x] Number of releases
- [x] Number of release definitions
- [x] Number of releases per definition
- [x] Number of successful releases per definition
- [x] Number of failed releases per definition
- [x] Number of cancelled releases per definition


- [ ] Number of tests passed
- [ ] Number of tests failed
