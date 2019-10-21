from ADOStats import Project
import csv
import target

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
    # name and total are not going to be dynamically added to the keys list as they dont exist in the API, so we need to pre-add them
    keys = ['name', 'total']
    for definition in listOfDefinitions:
        # Add all definition names to the list
        #   This will mean that even if they have no builds associated they are still represented
        myList.append({'name': definition.name, 'total': 0})
    for item in builds:
        for definitionDict in myList:
            # If this is the same definition (in list to be filled and list to take things from)
            if item.definition.name == definitionDict['name']:
                # If the result does not exist for this definition
                if not item.result in definitionDict:
                    # Create this result type and set to 1
                    definitionDict[item.result] = 1
                    # If this result does not exists in the keys list, add it
                    #   This is so that they keys list will have a list of all of the result types used,
                    #   if a result is not used by ANY definition then it will not exist in keys
                    #   More importantly, we dont actually know what all of the results are
                    #   (and if we did it might change), so we have to get the types for the headers dynamically
                    if not item.result in keys:
                        keys.append(item.result)
                else:
                    definitionDict[item.result] += 1
                # We always want to increment the total
                definitionDict['total'] += 1
                # As we have found the definition in both, we wont again, so we can break to avoid pointless looping
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


# Create project
myProject = Project(target.organisation, target.project, target.pat)

# Get the list of builds from the API
builds = myProject.getBuilds()

# Get the list of build definitions from the API
#   It would technically be quicker to build the list of definitions from
#   the list of builds (as build objects contain the name of the definition,
#   which is actually all we need). However this would mean that we dont record
#   any build definitions that DONT have builds associated with them
buildDefinitions = myProject.getBuildDefinitions()

# Get the data "object" (list of dictionaries) and the fields used
data, fields = buildData(builds, buildDefinitions)
filename = target.project + '.csv'
with open(filename, 'w') as csvFile:
    # This writer is used to write the title and the empty line at the
    #   end of the block (build, release ect)
    titleWriter = csv.writer(csvFile, delimiter=',')
    titleWriter.writerow(['Builds by definition'])

    # This writer is used to actually write the data to the file
    #   Note the filednames being set to the list of keys used
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)

    # Empty line
    titleWriter.writerow([''])
csvFile.close()

releases = myProject.getReleases()
releaseDefinitions = myProject.getReleaseDefinitions()
data, fields = releaseData(releases, releaseDefinitions)
filename = target.project + '.csv'
with open(filename, 'a') as csvFile:
    titleWriter = csv.writer(csvFile, delimiter=',')
    titleWriter.writerow(['Releases by definition'])
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
    titleWriter.writerow([''])
csvFile.close()
