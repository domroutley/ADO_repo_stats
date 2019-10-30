import target
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import sys


if len(sys.argv) > 1:
    resultsPerRequest = sys.argv[1]
else:
    resultsPerRequest = 2

organizationUrl = 'https://dev.azure.com/' + target.organisation
credentials = BasicAuthentication('', target.pat)
connection = Connection(base_url=organizationUrl, creds=credentials)

buildClient = connection.clients.get_build_client()
builds = buildClient.get_builds(target.project, status_filter='all')

total = []
for b in builds.value:
    total.append(b.id)

builds = buildClient.get_builds(target.project, top=resultsPerRequest, status_filter='all')
listOfBuilds = builds.value
while builds.continuation_token is not None:
    builds = buildClient.get_builds(target.project, status_filter='all', continuation_token=builds.continuation_token, top=resultsPerRequest)
    listOfBuilds.extend(builds.value)


got = []
for b in listOfBuilds:
    got.append(b.id)

print()
print('IDs of every build in ADO              : {}'.format(total))
print('Build ids returned by looping requests : {}'.format(got))
if total != got:
    print('List of build IDs returned from continuation requests does not match list of correct IDs')
else:
    print("Success")
