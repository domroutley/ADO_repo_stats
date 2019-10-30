import requests, json, sys
import target

def getRecursive(allBuilds, base_url, myAuth, resultsPerRequest, number=1, continuationToken=''):
    print('contoken used by request {} {}'.format(number, continuationToken))
    response = requests.get('{}build/builds?statusFilter=all&$top={}&continuationtoken={}&api-version=5.1'.format(base_url, resultsPerRequest, continuationToken), auth=myAuth)
    data = json.loads(response.text)

    print('IDs retrieved by request {} : '.format(number), end='')
    for build in data['value']:
        print('{} '.format(build['id']), end='')
    print()

    allBuilds['count'] += data['count']
    for build in data['value']:
        allBuilds['value'].append(build)


    if 'x-ms-continuationtoken' in response.headers:
        contoken = response.headers['x-ms-continuationtoken']
        print('contoken recieved by request {} {}\n'.format(number, contoken))
        if response.headers['x-ms-continuationtoken'] == continuationToken:
            print('continuation token recieved by request {} is the same as the the one used by request {} (infinite loop detected)'.format(number, number))
            return allBuilds
        number+=1
        allBuilds = getRecursive(allBuilds, base_url, myAuth, resultsPerRequest, number, contoken)

    return allBuilds




base_url = 'https://dev.azure.com/{}/{}/_apis/'.format(target.organisation, target.project)


rawResponse = requests.get('{}build/builds?statusFilter=all&api-version=5.1'.format(base_url), auth=requests.auth.HTTPBasicAuth('', target.pat))
rawData = json.loads(rawResponse.text)

total = []
for build in rawData['value']:
    total.append(build['id'])


if len(sys.argv) > 1:
    resultsPerRequest = sys.argv[1]
else:
    resultsPerRequest = 2

allBuilds = getRecursive({'count':0, 'value':[]}, base_url, requests.auth.HTTPBasicAuth('', target.pat), resultsPerRequest=resultsPerRequest)

got = []
for b in allBuilds['value']:
    got.append(b['id'])

print()
print('IDs of every build in ADO              : {}'.format(total))
print('Build ids returned by looping requests : {}'.format(got))
if total != got:
    print('List of build IDs returned from continuation requests does not match list of correct IDs')
else:
    print("Success")
