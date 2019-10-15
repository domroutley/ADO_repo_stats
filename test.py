from ADOStats import Project
f = open('token', 'r')
pat = f.read()
pat = pat[:-1] # Strip newline from end of token
test = Project('dominicroutley', 'learningTest', pat)
print(test.project.name)


test.getRepositories()
