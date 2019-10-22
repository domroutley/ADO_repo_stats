import AzureDevOpsWrapper

import csv, os

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

    buildStructure, buildFields = createBuildStructure(builds, buildDefinitions)
    writeFile(projectName, buildStructure, buildFields, "build")

    releaseStructure, releaseFields = createReleaseStructure(releases, releaseDefinitions)
    writeFile(projectName, releaseStructure, releaseFields, "release")


def writeFile(projectName, data, fields, mode):
    if not os.path.exists(projectName):
        os.mkdir(projectName)
    filename = projectName + '/' + projectName + '-' + mode + '.csv'
    with open(filename, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    csvFile.close()


def createBuildStructure(builds, listOfDefinitions):
    """Creates a list of dictionaries containing data about the builds in a build definition.

    :param builds: A list of build objects to be counted in the dictionaries
    :builds type: <List> of type <class 'azure.devops.v5_1.build.models.Build'>

    :param listOfDefinitions: A list of build definition objects to be added as dictionaries (name only)
    :listOfDefinitions type: <List> of type <class 'azure.devops.v5_1.build.models.BuildDefinitionReference'>

    :return: A list of dictionaries containing data about the builds in a build definition
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the dictionaries, we cannot gaurentee what the keys will be called, so we return all the ones used so that the CSV file can have them as column titles.
    :rtype: <List> of type <String>
    """
    myList = []
    # create list of keys
    keys = ['name', 'succeeded', 'partiallySucceeded', 'cancelled', 'failed', 'none', 'total']
    for definition in listOfDefinitions:
        # Add all definition names to the list
        #   This will mean that even if they have no builds associated they are still represented
        #   We also set all of the possible results to 0
        myList.append({'name': definition.name, 'succeeded': 0, 'partiallySucceeded': 0, 'cancelled': 0, 'failed': 0, 'none': 0, 'total': 0})
    for item in builds:
        for definitionDict in myList:
            # If this is the same definition (in list to be filled and list to take things from)
            if item.definition.name == definitionDict['name']:
                definitionDict[item.result] += 1
                # We always want to increment the total
                definitionDict['total'] += 1
                # As we have found the definition in both, we wont again, so we can break to avoid pointless looping
                break
    return myList, keys


def createReleaseStructure(releases, listOfDefinitions):
    """Creates a list of dictionaries containing data about the releases in a release definition.

    :param releases: A list of release objects to be counted in the dictionaries
    :releases type: <List> of type <class 'azure.devops.v5_1.release.models.Release'>

    :param listOfDefinitions: A list of release definition objects to be added as dictionaries (name only)
    :listOfDefinitions type: <List> of type <class 'azure.devops.v5_1.release.models.ReleaseDefinition'>

    :return: A list of dictionaries containing data about the releases in a release definition
    :rtype: <List> of type <Dictionary>

    :return: A list of the keys used in the dictionaries, we cannot gaurentee what the keys will be called, so we return all the ones used so that the CSV file can have them as column titles.
    :rtype: <List> of type <String>
    """
    myList = []
    keys = ['name', 'total']
    for definition in listOfDefinitions:
        myList.append({'name': definition.name, 'total': 0})
    for item in releases:
        for definitionDict in myList:
            if item.release_definition.name == definitionDict['name']:
                if not item.status in definitionDict:
                    definitionDict[item.status] = 1
                    if not item.status in keys:
                        keys.append(item.status)
                else:
                    definitionDict[item.status] += 1
                definitionDict['total'] += 1
                break
    return myList, keys


if __name__ == "__main__":
    import target
    main(target.organisation, target.project, target.pat)
