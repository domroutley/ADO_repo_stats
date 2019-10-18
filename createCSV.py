from ADOStats import Project
import csv

def buildData(builds, listOfDefinitions):
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

# Create project
myProject = Project('dominicroutley', 'learningTest', pat)

builds = myProject.getBuilds()
buildDefinitions = myProject.getBuildDefinitions()
data, fields = buildData(builds, buildDefinitions)
filename = proj + '.csv'
with open(filename, 'w') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
csvFile.close()

releases = myProject.getReleases()
releaseDefinitions = myProject.getReleaseDefinitions()
data, fields = releaseData(releases, releaseDefinitions)
filename = proj + '.csv'
with open(filename, 'a') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
csvFile.close()
