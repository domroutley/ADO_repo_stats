import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class Project:

    def __init__(self, organisation, projectName, personalAccessToken):
        self.org = organisation
        self.pn = projectName
        self.pat = personalAccessToken

        organizationUrl = 'https://dev.azure.com/' + self.org

        # Create a connection to the org
        credentials = BasicAuthentication('', self.pat)
        connection = Connection(base_url=organizationUrl, creds=credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        coreClient = connection.clients.get_core_client()

        # Get the first page of projects
        getProjectsResponse = coreClient.get_projects()
        index = 0
        while getProjectsResponse is not None:
            for project in getProjectsResponse.value:
                if (project.name == self.pn):
                    self.project = project
                    # Stop grabbing stuff
                    getProjectsResponse.continuation_token = None
                    break
                index += 1
            if getProjectsResponse.continuation_token is not None and getProjectsResponse.continuation_token != "":
                # Get the next page of projects
                getProjectsResponse = coreClient.get_projects(continuation_token=getProjectsResponse.continuation_token)
            else:
                # All projects have been retrieved
                getProjectsResponse = None

    def getRepositories(self):
        pass
