from ADOStats import Project

def createDictBuild(listOfItems, verbose=False):
    """Create a dictionary containing each build definition and the builds that are assigned to them.

    :param listOfItems: A list of build items
    :listOfItems type: <List> of type <class 'azure.devops.v5_1.build.models.Build'>

    :param verbose: Do we want to print the dictionary after creation
    :verbose type: <Boolean>

    :return: A dictionary of dictionaries containing the total results of builds
    :rtype: <Dictionary>
    """
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


def createDictRelease(listOfItems, verbose=False):
    """Create a dictionary containing each release definition and the releases that are assigned to them.

    :param listOfItems: A list of release items
    :listOfItems type: <List> of type <class 'azure.devops.v5_1.release.models.Release'>

    :param verbose: Do we want to print the dictionary after creation
    :verbose type: <Boolean>

    :return: A dictionary of dictionaries containing the total statuses of releases
    :rtype: <Dictionary>
    """
    dictionary = {}
    for item in listOfItems:
        # If this definition already exists in the dictionary
        if item.release_definition.name in dictionary:
            # Increment total count
            dictionary[item.release_definition.name]["total"] += 1
            # If outcome of item already exists in sub-dictionary
            if item.status in dictionary[item.release_definition.name]:
                # Increment outcome count
                dictionary[item.release_definition.name][item.status] += 1
            else:
                # Create it and set to 1
                dictionary[item.release_definition.name][item.status] = 1
        else:
            # Create sub-dictionary and set total to 1
            dictionary[item.release_definition.name] = {}
            dictionary[item.release_definition.name]["total"] = 1
            dictionary[item.release_definition.name][item.status] = 1

    if verbose:
        for item in dictionary:
            print(item + " " + str(dictionary[item]))

    return dictionary

# Get pat from file
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token

# Change these lines to use your own organisation and project name
organisation = 'dominicroutley'
project = 'learningTest'
# Create project
myProject = Project(organisation, project, pat)
print("Project: " + myProject.project.name)

# Get repositories
repos = myProject.getRepositories()
print("Repositories: " + str(len(repos)))

print()

# Get builds
builds = myProject.getBuilds()
print("Builds: " + str(len(builds)))

# Get build definitions
buildDefinitions = myProject.getBuildDefinitions()
print("Build definitions: " + str(len(buildDefinitions)))

# Get build status per build definition
buildDict = createDictBuild(builds, True)

print() # gap in printout

# Get releases
releases = myProject.getReleases()
print("Releases: " + str(len(releases)))

# Get release definitions
releaseDefinitions = myProject.getReleaseDefinitions()
print("Release definitions: " + str(len(releaseDefinitions)))

# Get release staus per release definition
releaseDict = createDictRelease(releases, True)
