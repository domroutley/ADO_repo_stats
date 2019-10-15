import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class Project:

    # initilises connection with ADO
    def __init__(self, organisation, projectName, personalAccessToken):
        self.org = organisation
        pn = projectName
        self.pat = personalAccessToken

        organizationUrl = 'https://dev.azure.com/' + self.org

        # Create a connection to the org
        credentials = BasicAuthentication('', self.pat)
        self.connection = Connection(base_url=organizationUrl, creds=credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        coreClient = self.connection.clients.get_core_client()

        # Get the first page of projects
        getProjectsResponse = coreClient.get_projects()
        index = 0
        while getProjectsResponse is not None:
            for project in getProjectsResponse.value:
                if (project.name == pn):
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

    # Returns a list of repository objects
    def getRepositories(self):
        from azure.devops.released.git import GitClient

        gitClient = self.connection.clients.get_git_client()
        repos = gitClient.get_repositories(self.project.name)
        return repos

    # Returns a list of build definition objects
    def getBuildDefinitions(self):
        from azure.devops.released.build import BuildClient

        buildClient = self.connection.clients.get_build_client()
        definitions = buildClient.get_definitions(self.project.name)
        listOfDefinitions = definitions.value

        # While there is more to get, get them and extend the current list
        while definitions.continuation_token is not None:
            definitions = buildClient.get_definitions(self.project.name, continuation_token=definitions.continuation_token)
            listOfDefinitions.extend(definitions.value)

        return listOfDefinitions

    # Returns a list of release objects
    def getReleases(self):
        return self.releases("releases")

    # Returns a list of release objects
    def getReleaseDefinitions(self):
        return self.releases("definitions")

    def releases(self, mode):
        from azure.devops.released.release import ReleaseClient

        releaseClient = self.connection.clients.get_release_client()
        if mode == "definitions":
            releases = releaseClient.get_release_definitions(self.project.name)
        elif mode == "releases":
            releases = releaseClient.get_releases(self.project.name)
        list = releases.value

        # While there is more to get, get them and extend the current list
        while releases.continuation_token is not None:
            if mode == "definitions":
                releases = releaseClient.get_release_definitions(self.project.name, continuation_token=releases.continuation_token)
            elif mode == "releases":
                releases = releaseClient.get_releases(self.project.name, continuation_token=releases.continuation_token)
            list.extend(releases.value)

        return list
