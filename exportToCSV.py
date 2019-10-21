from ADOStats import Project
import csv

def buildData(builds, listOfDefinitions):
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
    keys = ['name', 'total']
    for definition in listOfDefinitions:
        myList.append({'name': definition.name, 'total': 0})
    for item in builds:
        for definitionDict in myList:
            if item.definition.name == definitionDict['name']:
                if not item.result in definitionDict:
                    definitionDict[item.result] = 1
                    if not item.result in keys:
                        keys.append(item.result)
                else:
                    definitionDict[item.result] += 1
                definitionDict['total'] += 1
                break
    return myList, keys


def releaseData(releases, listOfDefinitions):
    """Creates a list of dictionaries containing data about the releases in a release definition.

    :param releases: A list of release objects to be counted in the dictionaries
    :builds type: <List> of type <class 'azure.devops.v5_1.release.models.Release'>

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

# Get pat from file
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token

# Change these lines to use your own organisation and project name
organisation = "dominicroutley"
project = "learningTest"
# Create project
myProject = Project(organisation, project, pat)

builds = myProject.getBuilds()
buildDefinitions = myProject.getBuildDefinitions()
data, fields = buildData(builds, buildDefinitions)
filename = project + '.csv'
with open(filename, 'w') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
csvFile.close()

releases = myProject.getReleases()
releaseDefinitions = myProject.getReleaseDefinitions()
data, fields = releaseData(releases, releaseDefinitions)
filename = project + '.csv'
with open(filename, 'a') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
csvFile.close()