from ADOStats import Project

def createDict(listOfItems, verbose=False):
    dictionary = {}
    for item in listOfItems:
        # If this definition already exists in the dictionary
        if item.definition.name in dictionary:
            # Increment total count
            dictionary[item.definition.name]["total"] += 1
            # If outcome of item already exists in sub-dictionary
            if item.result in dictionary[item.definition.name]:
                # Increment outcome count
                dictionary[item.definition.name][item.result] += 1
            else:
                # Create it and set to 1
                dictionary[item.definition.name][item.result] = 1
        else:
            # Create sub-dictionary and set total to 1
            dictionary[item.definition.name] = {}
            dictionary[item.definition.name]["total"] = 1
            dictionary[item.definition.name][item.result] = 1

    if verbose:
        for item in dictionary:
            print(item + " " + str(dictionary[item]))

    return dictionary

# Get pat from file
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token

# Create project
myProject = Project('dominicroutley', 'learningTest', pat)
print("Project: " + myProject.project.name)

# Get repositories
repos = myProject.getRepositories()
print("Repositories: " + str(len(repos)))

# Get builds
builds = myProject.getBuilds()
print("Builds: " + str(len(builds)))

buildDefinitions = myProject.getBuildDefinitions()
print("Build definitions: " + str(len(buildDefinitions)))

buildDict = createDict(builds, True)

print() # gap

releases = myProject.getReleases()
print("Releases: " + str(len(releases)))

releaseDefinitions = myProject.getReleaseDefinitions()
print("Release definitions: " + str(len(releaseDefinitions)))

releaseDict = createDict(releases, True)
