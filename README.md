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
- Run the `exampleUsage.py` file to see an example output. You will need to create a `token` file containing only a PAT for ADO (there must be a newline at the end of the token and nothing else in the file), and change the project initialisation call to use your organisation and project names.


## TODO
- ~~Number of repositories~~


- ~~Number of builds~~
- ~~Number of build definitions~~
- ~~Number of builds per definition~~
- ~~Number of successful builds per definition~~
- ~~Number of failed builds per definition~~
- ~~Number of cancelled builds per definition~~


- ~~Number of releases~~
- ~~Number of release definitions~~
- ~~Number of releases per definition~~
- ~~Number of successful releases per definition~~
- ~~Number of failed releases per definition~~
- ~~Number of cancelled releases per definition~~


- Number of tests passed
- Number of tests failed
