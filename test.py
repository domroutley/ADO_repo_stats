import requests, json
import target

def getRecursive(allBuilds, base_url, myAuth, number=1, continuationToken=''):
    response = requests.get('{}build/builds?statusFilter=all&$top=2&continuationtoken={}&api-version=5.1'.format(base_url, continuationToken), auth=myAuth)
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
        if contoken == continuationToken:
            print('same con tokens detected')
            print('count value as of here {}'.format(allBuilds['count']))
            print('number of builds as of here {}'.format(len(allBuilds['value'])))
            print('build ids as of here ', end='')
            for b in allBuilds['value']:
                print('{} '.format(b['id']), end='')
            print('\n')
            exit()
        number+=1
        allBuilds = getRecursive(allBuilds, base_url, myAuth, number, contoken)

    return allBuilds




base_url = 'https://dev.azure.com/{}/{}/_apis/'.format(target.organisation, target.project)


rawResponse = requests.get('{}build/builds?statusFilter=all&api-version=5.1'.format(base_url), auth=requests.auth.HTTPBasicAuth('', target.pat))
rawData = json.loads(rawResponse.text)

print('IDs of every build : ')
for build in rawData['value']:
    print('{} '.format(build['id']), end='')
print('\n')

allBuilds = getRecursive({'count':0, 'value':[]}, base_url, requests.auth.HTTPBasicAuth('', target.pat))

print('\nbuild ids at the end ')
for b in allBuilds['value']:
    print('{} '.format(b['id']), end='')
print('\n')



pass
