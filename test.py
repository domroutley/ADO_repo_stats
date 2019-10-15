from ADOStats import Project
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token
test = Project('dominicroutley', 'learningTest', pat)
print("Project: " + test.project.name)


repos = test.getRepositories()
for repo in repos:
    print("Repository      : " + repo.name)

defs = test.getDefinitions()
for defi in defs:
    print("Build definition: " + defi.name)
