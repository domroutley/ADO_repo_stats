from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import requests, json

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
        self.projectName = projectName
        self.pat = personalAccessToken

        self.base_url = 'https://dev.azure.com/{}/{}/_apis/'.format(organisation, projectName)
        self.release_base_url = 'https://vsrm.dev.azure.com/{}/{}/_apis/'.format(organisation, projectName)

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
                if (project.name == self.projectName):
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
                raise Exception('Project {} was not found.'.format(self.projectName))


    def getRepositories(self):
        """Get the list of repositories from the project.

        :return: A list of repositories
        :rtype: <Dictionary>
        """
        response = requests.get('{}git/repositories?api-version=5.1'.format(self.base_url), auth=requests.auth.HTTPBasicAuth('', self.pat))
        return json.loads(response.text)


    def getRepositoryCommits(self, repo, branch=''):
        """Return the commits for a repository.
        ..:note: This function uses a direct call to the API as opposed to using the python wrapper module, this is because in v5.1 of the python wrapper there is no way to currently return the data we require

        :param repo: A repository object to get the stats for
        :repo type: <class 'azure.devops.v5_1.git.models.GitRepository'>

        :param branch: What branch to target, blank for all
        :branch type:

        :return: All of the commits for that repository as a dictionary
        :rtype: <Dictionary>
        """
        if branch is not None:
            branch = 'searchCriteria.itemVersion.version={}&'.format(branch)
        response = requests.get('{}git/repositories/{}/commits?searchCriteria.$top=10000&{}api-version=5.1'.format(self.base_url, repo['id'], branch), auth=requests.auth.HTTPBasicAuth('', self.pat))
        return json.loads(response.text)


    def getBuilds(self):
        """Get the list of builds from the project.
        .. notes:: This method is a wrapper that simply calls the builds method with the mode argument set to "builds"

        :return: A list of builds
        :rtype: <List> of type <class 'azure.devops.v5_1.build.models.Build'>
        """
        return self.builds()


    def getBuildDefinitions(self):
        """Get the list of build definitions from the project.

        :return: A dictionary of build definitions
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}build/definitions?queryOrder=lastModifiedDescending&api-version=5.1'.format(self.base_url), auth=requests.auth.HTTPBasicAuth('', self.pat))
        allDefinitions = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}build/definitions?continuationtoken={}&queryOrder=lastModifiedDescending&api-version=5.1'.format(self.base_url, rawResponse.headers['x-ms-continuationtoken']), auth=requests.auth.HTTPBasicAuth('', self.pat))
            response = json.loads(rawResponse.text)
            allDefinitions['count'] += response['count']
            allDefinitions['value'].extend(response['value'])
        return allDefinitions


    def builds(self):
        """Use the build client to get builds or build definitions from the ADO API.
        .. notes:: This method is intented to be used by the wrapper functions.

        :return: A list of builds
        :rtype: <List> of type <class 'azure.devops.v5_1.build.models.Build'>
        """
        buildClient = self.connection.clients.get_build_client()
        builds = buildClient.get_builds(self.project.name)
        listOfBuilds = builds.value

        # While there is more to get, get them and extend the current list
        while builds.continuation_token is not None:
            builds = buildClient.get_builds(self.project.name, continuation_token=builds.continuation_token)
            listOfBuilds.extend(builds.value)

        return listOfBuilds


    def getDeployments(self):
        """Get the list of release deployments from the project.

        :return: A dictionary of releases
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}release/deployments?api-version=5.1'.format(self.release_base_url), auth=requests.auth.HTTPBasicAuth('', self.pat))
        allReleases = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}release/deployments?continuationtoken={}&api-version=5.1'.format(self.release_base_url, rawResponse.headers['x-ms-continuationtoken']), auth=requests.auth.HTTPBasicAuth('', self.pat))
            response = json.loads(rawResponse.text)
            allReleases['count'] += response['count']
            allReleases['value'].extend(response['value'])

        return allReleases


    def getReleaseDefinitions(self):
        """Get the list of release definitions from the project.

        :return: A dictionary of release definitions
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}release/definitions?api-version=5.1'.format(self.release_base_url), auth=requests.auth.HTTPBasicAuth('', self.pat))
        allDefinitions = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}release/definitions?continuationtoken={}&api-version=5.1'.format(self.release_base_url, rawResponse.headers['x-ms-continuationtoken']), auth=requests.auth.HTTPBasicAuth('', self.pat))
            response = json.loads(rawResponse.text)
            allDefinitions['count'] += response['count']
            allDefinitions['value'].extend(response['value'])

        return allDefinitions
