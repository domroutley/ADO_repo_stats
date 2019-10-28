import AzureDevOpsWrapper

import csv, os, json

def main(organisationName, projectName, pat):
    """Creates five csv files containing raw statistics about the given project.

    :param organisationName: The name of the organisation that contains the target project.
    :organisationName type: <String>

    :param projectName: The name of the target project.
    :projectName type: <String>

    :param pat: A valid personal access token to be used for access to the project.
    :pat type: <String>

    :return: None
    """

    theProject = AzureDevOpsWrapper.Project(organisationName, projectName, pat)

    repositories = theProject.getRepositories()
    builds = theProject.getBuilds()
    buildDefinitions = theProject.getBuildDefinitions()
    releases = theProject.getReleases()
    releaseDefinitions = theProject.getReleaseDefinitions()

    buildStructure, buildFields, buildTimeList, buildTimeListKeys = createBuildStructures(builds, buildDefinitions)
    releaseStructure, releaseFields, releaseTimeList, releaseTimeListKeys = createReleaseStructures(releases, releaseDefinitions)
    gitStructure, gitFields, commitsInTotal = createGitStructures(repositories, theProject)


    writeFile(projectName, ['number of builds', len(builds)], [], 'overview', 'w')
    writeFile(projectName, ['number of build definitions', len(buildDefinitions)], [], 'overview')
    writeFile(projectName, ['number of releases', len(releases)], [], 'overview')
    writeFile(projectName, ['number of release definitions', len(releaseDefinitions)], [], 'overview')
    writeFile(projectName, ['number of repositories', repositories['count']], [], 'overview')
    writeFile(projectName, ['number of commits', commitsInTotal], [], 'overview')


    writeFile(projectName, buildStructure, buildFields, 'build', 'w')
    writeFile(projectName, [], [], 'build')
    writeFile(projectName, ['number of build definitions', len(buildDefinitions)], [], 'build')
    writeFile(projectName, [], [], 'build')
    writeFile(projectName, ['number of builds', len(builds)], [], 'build')
    writeFile(projectName, [], [], 'build')
    writeFile(projectName, buildTimeList, buildTimeListKeys, 'build')


    writeFile(projectName, releaseStructure, releaseFields, 'release', 'w')
    writeFile(projectName, [], [], 'release')
    writeFile(projectName, ['number of release definitions', len(releaseDefinitions)], [], 'release')
    writeFile(projectName, [], [], 'release')
    writeFile(projectName, ['number of releases', len(releases)], [], 'release')
    writeFile(projectName, [], [], 'release')
    writeFile(projectName, releaseTimeList, releaseTimeListKeys, 'release')


    writeFile(projectName, gitStructure, gitFields, 'git', 'w')
    writeFile(projectName, [], [], 'git')
    writeFile(projectName, ['number of repositories', repositories['count']], [], 'git')
    writeFile(projectName, [], [], 'git')
    writeFile(projectName, ['number of commits in total', commitsInTotal], [], 'git')


def writeFile(projectName, data, fields, file, mode='a'):
    """Writes the given data to a csv file.
    ..:notes: If data and fields are set to empty list, this function will add an empty line
    If fields is set to empty list (and data is not), this function will add to the csv without headers

    :param projectName: The name of the project (used in file/foldername)
    :projectName type: <String>

    :param data: The data to be written, usually the output of createBuildStructure or createReleaseStructure
    :data type: <List> of type <Dictionary>

    :param fields: The field titles to put at the top of the file
    :fields type: <List> of type <String>

    :param file: What to put at the end of the filename to distinguish it (build, release)
    :file type: <String>

    :param mode: What mode to write in (drirect pass through to open([filename], mode))
    :file type: <char>
    :default: 'a'

    :return: None
    """
    if not os.path.exists(projectName):
        os.mkdir(projectName)
    filename = projectName + '/' + projectName + '-' + file + '.csv'
    with open(filename, mode) as csvFile:
        if fields == []:
            writer = csv.writer(csvFile)
            writer.writerow(data)
        else:
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    csvFile.close()


def createBuildStructures(builds, listOfDefinitions):
    """Creates a list of dictionaries containing data about the builds in a build definition.

    :param builds: A list of build objects to be counted in the dictionaries
    :builds type: <List> of type <class 'azure.devops.v5_1.build.models.Build'>

    :param listOfDefinitions: A list of build definition objects to be added as dictionaries (name only)
    :listOfDefinitions type: <List> of type <class 'azure.devops.v5_1.build.models.BuildDefinitionReference'>

    :return: A list of dictionaries containing data about the builds in a build definition
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the dictionaries, we cannot gaurentee what the keys will be called, so we return all the ones used so that the CSV file can have them as column titles.
    :rtype: <List> of type <String>

    :return: A list of dictionaries containing the duration of builds
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the time dictionary
    :rtype: <List> of type <String>
    """
    myList = []
    keys = []
    buildTimeList = []
    timeListKeys = []
    if len(listOfDefinitions) > 0:
        for definition in listOfDefinitions:
            # Add all definition names to the list
            #   This will mean that even if they have no builds associated they are still represented
            #   We also set all of the possible results to 0
            # Hi future maintainer, the order of the keys here is the order that they appear in the csv file
            myList.append({
            'definition': definition.name,
            'succeeded': 0,
            'partiallySucceeded': 0,
            'canceled': 0,
            'failed': 0,
            'none': 0,
            'total': 0,
            'avg duration': 0
            })
        # create list of keys, pulls keys from above dictionary
        for key in myList[0]:
            keys.append(key)

    if len(builds) > 0:
        for item in builds:
            # If the deployment has not started then the start_time and finish_time times will not have its timezone info set, but the queue_time time will
            # This will cause a TypeError when trying to do maths with a non-timezone aware datetime and a timezone aware datetime
            if item.start_time.tzinfo is None:
                queueDuration = 0
            else:
                queueDuration = (item.start_time - item.queue_time).total_seconds()
            # See comment above
            if item.finish_time.tzinfo is None:
                duration = 0
            else:
                # Get the duration of the build
                duration = (item.finish_time - item.start_time).total_seconds()
            # Add to buildTimeList
            buildTimeList.append({
            'build id': item.id,
            'definition': item.definition.name,
            'result': item.result,
            'queued at time': item.queue_time.strftime("%H:%M:%S"),
            'queued at date': item.queue_time.strftime("%d/%m/%Y"),
            'duration': duration,
            'queue duration': queueDuration
            })
            # This may happen if the build hasnt finished yet
            if item.result is None:
                continue
            for definitionDict in myList:
                # If this is the same definition (in list to be filled and list to take things from)
                if item.definition.name == definitionDict['definition']:
                    definitionDict[item.result] += 1
                    # We always want to increment the total
                    definitionDict['total'] += 1
                    # Add duration to sum of all durations (this will be converted to an average later)
                    definitionDict['avg duration'] += duration
                    # As we have found the definition in both, we wont again, so we can break to avoid pointless looping
                    break
        # create list of keys, pulls keys from above dictionary
        for key in buildTimeList[0]:
            timeListKeys.append(key)

    if len(listOfDefinitions) > 0:
        for definition in myList:
            # Calculate average
            if not definition['total'] == 0:
                definition['avg duration'] = definition['avg duration'] / definition['total']

    return myList, keys, buildTimeList, timeListKeys


def createReleaseStructures(releases, listOfDefinitions):
    """Creates a list of dictionaries containing data about the releases in a release definition.

    :param releases: A list of release objects to be counted in the dictionaries
    :releases type: <List> of type <class 'azure.devops.v5_1.release.models.Release'>

    :param listOfDefinitions: A list of release definition objects to be added as dictionaries (name only)
    :listOfDefinitions type: <List> of type <class 'azure.devops.v5_1.release.models.ReleaseDefinition'>

    :return: A list of dictionaries containing data about the releases in a release definition
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the dictionaries, we cannot gaurentee what the keys will be called, so we return all the ones used so that the CSV file can have them as column titles.
    :rtype: <List> of type <String>

    :return: A list of dictionaries containing the duration of deployments
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the time dictionary
    :rtype: <List> of type <String>
    """
    myList = []
    keys = []
    releaseTimeList = []
    timeListKeys = []
    if len(listOfDefinitions) > 0:
        for definition in listOfDefinitions:
            # Hi future maintainer, the order of the keys here is the order that they appear in the csv file
            myList.append({
            'definition': definition.name,
            'succeeded': 0,
            'partiallySucceeded': 0,
            'cancelled': 0,
            'failed': 0,
            'inProgress': 0,
            'notDeployed': 0,
            'all': 0,
            'undefined': 0,
            'total': 0,
            'avg duration': 0
            })
        # create list of keys, pulls keys from above dictionary
        for key in myList[0]:
            keys.append(key)

    if len(releases) > 0:
        for item in releases:
            # If the deployment has not started then the started_on and completed_on times will not have its timezone info set, but the queued_on time will
            # This will cause a TypeError when trying to do maths with a non-timezone aware datetime and a timezone aware datetime
            if item.started_on.tzinfo is None:
                queueDuration = 0
            else:
                queueDuration = (item.started_on - item.queued_on).total_seconds()
            # See comment above
            if item.completed_on.tzinfo is None:
                duration = 0
            else:
                # Get the duration of the deployment
                duration = (item.completed_on - item.started_on).total_seconds()
            # Add to releaseTimeList
            releaseTimeList.append({
            'deployment id': item.id,
            'definition': item.release_definition.name,
            'result': item.deployment_status,
            'queued at time': item.queued_on.strftime("%H:%M:%S"),
            'queued at date': item.queued_on.strftime("%d/%m/%Y"),
            'duration': duration,
            'queue duration': queueDuration
            })
            for definitionDict in myList:
                if item.release_definition.name == definitionDict['definition']:
                    definitionDict[item.deployment_status] += 1
                    definitionDict['total'] += 1
                    definitionDict['avg duration'] += duration
                    break
        # create list of keys
        for key in releaseTimeList[0]:
            timeListKeys.append(key)

    if len(listOfDefinitions) > 0:
        for definition in myList:
            # Calculate average
            if not definition['total'] == 0:
                definition['avg duration'] = definition['avg duration'] / definition['total']

    return myList, keys, releaseTimeList, timeListKeys


def createGitStructures(repositories, theProject):
    """Creates a list of dictionaries containing data about the repositories.

    :param repositories: A List of repositories
    :repositories type: <List>

    :param theProject: The AzureDevOpsWrapper Project
    :theProject type: <class 'AzureDevOpsWrapper.Project'>

    :return: A list of dictionaries, one for each repository
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the dictionaries, this is used for the headers of the csv file
    :rtype: <List> of type <String>
    """
    keys = []
    myList = []
    commitsInTotal = 0
    if len(repositories) > 0:
        for repository in repositories['value']:
            additions = deletions = editions = 0
            # If the repo is not totally empty
            if 'defaultBranch' in repository:
                defaultBranch = repository['defaultBranch'][11:]
                repositoryCommits = theProject.getRepositoryCommits(repository)
                defaultBranchCommits = theProject.getRepositoryCommits(repository, branch=defaultBranch)
                for commit in repositoryCommits['value']:
                    additions += int(commit['changeCounts']['Add'])
                    deletions += int(commit['changeCounts']['Delete'])
                    editions += int(commit['changeCounts']['Edit'])
            else:
                # Set some defaults
                defaultBranch = ''
                defaultBranchCommits = {'count': 0}
                repositoryCommits = {'count': 0}

            myList.append({
            'repository': repository['name'],
            'default branch': defaultBranch,
            'number of commits (default branch)': defaultBranchCommits['count'],
            'number of commits (all branches)': repositoryCommits['count'],
            'number of additions (default branch)': additions,
            'number of deletions (default branch)': deletions,
            'number of edits (default branch)': editions
            })
            commitsInTotal += repositoryCommits['count']
        # create list of keys, pulls keys from above dictionary
        for key in myList[0]:
            keys.append(key)

    return myList, keys, commitsInTotal


if __name__ == "__main__":
    import target
    main(target.organisation, target.project, target.pat)
