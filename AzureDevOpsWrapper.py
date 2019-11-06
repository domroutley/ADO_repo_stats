import requests, json

class Project:

    def __init__(self, organisation, projectName, personalAccessToken):
        """Initalise the object variables.

        :param organisation: The organisation that the project is owned by
        :organisation type: <String>

        :param projectName: The name of the project to get statistics from
        :projectName type: <String>

        :param personalAccessToken: A valid Personal Access Token that allows access to the project
        :personalAccessToken type: <String>

        :return: no value
        :rtype: no value
        """
        self.auth = requests.auth.HTTPBasicAuth('', personalAccessToken)
        self.base_url = 'https://dev.azure.com/{}/{}/_apis/'.format(organisation, projectName)
        self.release_base_url = 'https://vsrm.dev.azure.com/{}/{}/_apis/'.format(organisation, projectName)


    def getRepositories(self):
        """Get the list of repositories from the project.

        :return: A list of repositories
        :rtype: <Dictionary>
        """
        response = requests.get('{}git/repositories?api-version=5.1'.format(self.base_url), auth=self.auth)
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
        response = requests.get('{}git/repositories/{}/commits?searchCriteria.$top=10000&{}api-version=5.1'.format(self.base_url, repo['id'], branch), auth=self.auth)
        return json.loads(response.text)


    def getBuilds(self):
        """Get the list of builds from the project.

        :return: A dictionary of all builds
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}build/builds?statusFilter=all&api-version=5.1'.format(self.base_url), auth=self.auth)
        allBuilds = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}build/builds?continuationToken={}&statusFilter=all&api-version=5.1'.format(self.base_url, token), auth=self.auth)
            response = json.loads(rawResponse.text)
            allBuilds['count'] += response['count']
            allBuilds['value'].extend(response['value'])

        return allBuilds


    def getBuildDefinitions(self):
        """Get the list of build definitions from the project.

        :return: A dictionary of build definitions
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}build/definitions?queryOrder=lastModifiedDescending&api-version=5.1'.format(self.base_url), auth=self.auth)
        allDefinitions = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}build/definitions?continuationtoken={}&queryOrder=lastModifiedDescending&api-version=5.1'.format(self.base_url, rawResponse.headers['x-ms-continuationtoken']), auth=self.auth)
            response = json.loads(rawResponse.text)
            allDefinitions['count'] += response['count']
            allDefinitions['value'].extend(response['value'])
        return allDefinitions


    def getDeployments(self):
        """Get the list of release deployments from the project.

        :return: A dictionary of releases
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}release/deployments?api-version=5.1'.format(self.release_base_url), auth=self.auth)
        allReleases = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}release/deployments?continuationtoken={}&api-version=5.1'.format(self.release_base_url, rawResponse.headers['x-ms-continuationtoken']), auth=self.auth)
            response = json.loads(rawResponse.text)
            allReleases['count'] += response['count']
            allReleases['value'].extend(response['value'])

        return allReleases


    def getReleaseDefinitions(self):
        """Get the list of release definitions from the project.

        :return: A dictionary of release definitions
        :rtype: <Dictionary>
        """
        rawResponse = requests.get('{}release/definitions?api-version=5.1'.format(self.release_base_url), auth=self.auth)
        allDefinitions = json.loads(rawResponse.text)
        while 'x-ms-continuationtoken' in rawResponse.headers:
            rawResponse = requests.get('{}release/definitions?continuationtoken={}&api-version=5.1'.format(self.release_base_url, rawResponse.headers['x-ms-continuationtoken']), auth=self.auth)
            response = json.loads(rawResponse.text)
            allDefinitions['count'] += response['count']
            allDefinitions['value'].extend(response['value'])

        return allDefinitions
