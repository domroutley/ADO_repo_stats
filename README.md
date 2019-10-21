# Azure DevOps repository statistics python module

*It is strongly suggested that you use a virtual python environment.  
Install:`python3 -m venv .venv`  
Run:`source .venv/bin/activate`  
Test:`which python3`  
(should give path to .venv/bin/python3, not global python location)  
Stop:`deactivate`*

## To run
(Make sure you are using Python 3)
- Clone repo  
  `git clone https://github.com/domroutley/ADO_repo_stats.git`
- Install required packages  
  `pip install -r requirements.txt`
- Change the organisation and project variables in the `target.py` file
- Run either `printToScreen` or `exportToCSV` from the examples folder to see the output.
  - You will need a file called `token` containing a PAT and to change the initial call to the class to have your organisation and project.


## TODO
### Git
- ~~Number of repositories~~

### Builds
- ~~Number of builds~~
- ~~Number of build definitions~~
- ~~Number of builds per definition~~
- ~~Number of successful builds per definition~~
- ~~Number of failed builds per definition~~
- ~~Number of cancelled builds per definition~~


### Releases
- ~~Number of releases~~
- ~~Number of release definitions~~
- ~~Number of releases per definition and their status~~
- Release status to be of class deployment


### Tests (on hold)
- Number of tests passed
- Number of tests failed
