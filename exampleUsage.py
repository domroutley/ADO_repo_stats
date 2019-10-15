def printAmount(number, what, project):
    print("There are " + str(number) + " " + what + " in the " + project.project.name + " project.")

from ADOStats import Project
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token
test = Project('dominicroutley', 'learningTest', pat)
print("Project: " + test.project.name)


repos = test.getRepositories()
printAmount(len(repos), "Repositories", test)

b = test.getBuilds()
printAmount(len(b), "Builds", test)
b = test.getBuildDefinitions()
printAmount(len(b), "Build definitions", test)


r = test.getReleases()
printAmount(len(r), "Releases", test)
r = test.getReleaseDefinitions()
printAmount(len(r), "Release definitions", test)
