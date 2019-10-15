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
# for repo in repos:
#     print("Repository      : " + repo.name)

defs = test.getBuildDefinitions()
printAmount(len(defs), "Build definitions", test)
# for defi in defs:
#     print("Build definition: " + defi.name)

rels = test.getReleases()
printAmount(len(rels), "Releases", test)
rels = test.getReleaseDefinitions()
printAmount(len(rels), "Release definitions", test)
