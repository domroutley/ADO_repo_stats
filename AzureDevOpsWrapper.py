from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class Project:

    def __init__(self, organisation, projectName, personalAccessToken):
        """Initilise the connection with Azure DevOps.

        :param organisation: The organisation that the project is owned by
        :organisation type: <String>

        :param projectName: The name of the project to get statistics from
        :projectName type: <String>

        :param personalAccessToken: A valid Personal Access Token that allows access to the project
        :personalAccessToken type: <String>

        :return: no value
        :rtype: no value
        """
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
        while getProjectsResponse is not None:
            for project in getProjectsResponse.value:
                if (project.name == pn):
                    self.project = project
                    # Stop grabbing stuff
                    getProjectsResponse.continuation_token = None
                    return
            if getProjectsResponse.continuation_token is not None and getProjectsResponse.continuation_token != "":
                # Get the next page of projects
                getProjectsResponse = coreClient.get_projects(continuation_token=getProjectsResponse.continuation_token)
            else:
                # All projects have been retrieved
                getProjectsResponse = None
                raise Exception('Project "' + pn + '" was not found.')


    def getRepositories(self):
        """Get the list of repositories from the project.

        :return: A list of repositories
        :rtype: <List> of type <class 'azure.devops.v5_1.git.models.GitRepository'>
        """

        gitClient = self.connection.clients.get_git_client()
        return gitClient.get_repositories(self.project.name)


    def getRepositoryStats(self, repo):
        """Return the statistics for a repository.

        !!!
        NOT USED
        This function relies on .getStats which is not yet released (maybe 6.0)
        See this for a related answer https://github.com/microsoft/azure-devops-python-api/issues/273
        !!!

        :param repo: A repository object to get the stats for
        :repo type: <class 'azure.devops.v5_1.git.models.GitRepository'>

        :return: None
        """
        return None # Filler
        gitClient = self.connection.clients.get_git_client()
        return gitClient.get_stats(self.project.name, repo.id)


    def getBuilds(self):
        """Get the list of builds from the project.
        .. notes:: This method is a wrapper that simply calls the builds method with the mode argument set to "builds"

        :return: A list of builds
        :rtype: <List> of type <class 'azure.devops.v5_1.build.models.Build'>
        """
        return self.builds("builds")


    def getBuildDefinitions(self):
        """Get the list of build definitions from the project.
        .. notes:: This method is a wrapper that simply calls the builds method with the mode argument set to "definitions"

        :return: A list of build definitions
        :rtype: <List> of type <class 'azure.devops.v5_1.build.models.BuildDefinitionReference'>
        """
        return self.builds("definitions")


    def builds(self, mode):
        """Use the build client to get builds or build definitions from the ADO API.
        .. notes:: This method is intented to be used by the wrapper functions.

        :param mode: The type of object to return, possible options: 'definitions' 'builds'
        :mode type: <String>

        :return: A list of either builds or build definitions
        :rtype: <List> of type <class 'azure.devops.v5_1.build.models.BuildDefinitionReference'> OR type <class 'azure.devops.v5_1.build.models.Build'>
        """

        buildClient = self.connection.clients.get_build_client()
        if mode == "definitions":
            builds = buildClient.get_definitions(self.project.name)
        elif mode == "builds":
            builds = buildClient.get_builds(self.project.name)
        listOfBuilds = builds.value

        # While there is more to get, get them and extend the current list
        while builds.continuation_token is not None:
            if mode == "definitions":
                builds = buildClient.get_definitions(self.project.name, continuation_token=builds.continuation_token)
            elif mode == "builds":
                builds = buildClient.get_builds(self.project.name, continuation_token=builds.continuation_token)
            listOfBuilds.extend(builds.value)

        return listOfBuilds


    def getReleases(self):
        """Get the list of releases from the project.
        .. notes:: This method is a wrapper that simply calls the releases method with the mode argument set to "releases"

        :return: A list of releases
        :rtype: <List> of type <class 'azure.devops.v5_1.release.models.Release'>
        """
        return self.releases("releases")


    def getReleaseDefinitions(self):
        """Get the list of release definitions from the project.
        .. notes:: This method is a wrapper that simply calls the releases method with the mode argument set to "definitions"

        :return: A list of release definitions
        :rtype: <List> of type <class 'azure.devops.v5_1.release.models.ReleaseDefinition'>
        """
        return self.releases("definitions")


    def releases(self, mode):
        """Use the release client to get releases or release definitions from the ADO API.
        .. notes:: This method is intented to be used by the wrapper functions.

        :param mode: The type of object to return, possible options: 'definitions' 'releases'
        :mode type: <String>

        :return: A list of releases or release definitions
        :rtype: <List> of type <class 'azure.devops.v5_1.release.models.ReleaseDefinition'> OR type <class 'azure.devops.v5_1.release.models.Release'>
        """

        releaseClient = self.connection.clients.get_release_client()
        if mode == "definitions":
            releases = releaseClient.get_release_definitions(self.project.name)
        elif mode == "releases":
            releases = releaseClient.get_deployments(self.project.name)
        listOfReleases = releases.value

        # While there is more to get, get them and extend the current list
        while releases.continuation_token is not None:
            if mode == "definitions":
                releases = releaseClient.get_release_definitions(self.project.name, continuation_token=releases.continuation_token)
            elif mode == "releases":
                releases = releaseClient.get_deployments(self.project.name, continuation_token=releases.continuation_token)
            listOfReleases.extend(releases.value)

        return listOfReleases
