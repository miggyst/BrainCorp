import json
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

PARAMETERS = ['name', 'uid', 'gid', 'comment', 'home', 'shell']

'''
<summary>Index function that returns Hello World!; Outputs the string onto the flask landing page</summary>
<returns>Hello World!</returns>
'''
@app.route('/')
def index():
    return 'Hello World!'

'''
<summary>GET request for /users web link</summary>
<returns>List of user information in readable JSON format</returns>
'''
@app.route('/users', methods=['GET'])
def getUsers():
    userList = userListFromPwdFile()
    if userList == 'Error':
        return 'Error'
    else:
        return jsonify(userList)

'''
<summary>GET request for /users/query web link</summary>
<returns>
List of user information in readable JSON format, dependent on specified details;
Will return 'Error' if a wrong/out-of-bounds key is used. Should be from PARAMETERS as seen above
</returns>
'''
@app.route('/users/query', methods=['GET'])
def getUsersQuery():
    paramList = []
    queryList = request.args.to_dict(flat=False)
    copyQueryList = queryList.copy()
    for queryParams in queryList:
        paramListData = {}
        key, value = copyQueryList.popitem()
        paramListData[key] = value[0]
        jsonParamListData = json.dumps(paramListData)
        paramList.append(jsonParamListData)
    userList = usersQuery(paramList)
    return jsonify(userList)


'''
<summary>GET request for /users/<uid> web link</summary>
<returns>
List of user information in readable JSON format, dependent on UID;
Will return a '404' Error if UID is not found
</returns>
<params name='uid'>url parameter object, needed to take note of the request paramter</params>
'''
@app.route('/users/<int:uid>', methods=['GET'])
def getUsersUid(uid):
    paramList = []
    usersUid = request.view_args['uid']
    paramListData = {}
    paramListData['uid'] = str(usersUid)
    paramList.append(json.dumps(paramListData))
    userList = usersQuery(paramList)
    if not userList:
        return 'Error: 404 uid \'' + str(usersUid) + '\' is not found' 
    else:
        return jsonify(userList[0])

'''
<summary>GET request for /users/<uid>/groups web link</summary>
<returns>
User information with a list of tied groups, dependent on UID;
Will return 'Error' if wrong UID is passed
</returns>
<params name='uid'>url parameter object, needed to take note of the request parameter</params>
'''
@app.route('/users/<int:uid>/groups', methods=['GET'])
def getUsersUidGroups(uid):
    paramList = []
    paramListData = {}
    usersUidGroups = {}
    jsonUsersUidGroups = []
    try:
        usersUid = request.view_args['uid']
        paramListData['uid'] = str(usersUid)
        paramList.append(json.dumps(paramListData))
        userList = usersQuery(paramList)
        userGid = userList[0]['gid']
        groupList = usersGroupsFromUid(usersUid,userGid)
        usersUidGroups['name'] = userList[0]['name']
        usersUidGroups['uid'] = str(userList[0]['uid'])
        usersUidGroups['members'] = groupList
        usersUidGroups = json.dumps(usersUidGroups)
        jsonUsersUidGroups.append(json.loads(usersUidGroups))
    except Exception:
        return 'Error'
    return jsonify(jsonUsersUidGroups)

'''
<summary>GET request for /groups web link</summary>
<returns>List of group information in readable JSON format</returns>
'''
@app.route('/groups', methods=['GET'])
def getGroups():
    groupList = groupListFromGroupFile()
    if groupList == 'Error':
        return 'Error'
    else:
        return jsonify(groupList)

@app.route('/groups/<int:gid>', methods=['GET'])
def getGroupGid(gid):
    paramList = []
    groupsGid = request.view_args['gid']
    paramListData = {}
    paramListData['gid'] = str(groupsGid)
    paramList.append(json.dumps(paramListData))
    gidList = groupsQuery(paramList)
    if not gidList:
        return 'Error: 404 gid \'' + str(groupsGid) + '\' is not found' 
    else:
        return jsonify(gidList[0])

#-------------------------------HTTP Request are above; General Functions are below-------------------------------#

'''
<summary>userListFromPwdFile function that searches and retrieves user data from /etc/passwd file</summary>
<returns>List object of user information (name,uid,gid,home, and shell) except for the encrypted password</returns>
'''
def userListFromPwdFile():
    userList = []
    try:
        with open('/etc/passwd') as file:
            userList = file.read().splitlines()
        for i in range(len(userList)):
            userList[i] = userList[i].split(':')
            userList[i] = {
                'name':userList[i][0],
                'uid':userList[i][2],
                'gid':userList[i][3],
                'comment':userList[i][4],
                'home':userList[i][5],
                'shell':userList[i][6]
            }
    except Exception as e:
        print(e)
        return 'Error'
    return userList

'''
<summary>The usersQuery function searches through current userList found in /etc/passwd and cross references GET request parameters to find specific users</summary>
<returns>List of user objects</returns>
<params name='parameterList'>list of paramters passed with the GET request</params>
'''
def usersQuery(parameterList):
    usersQueryList = []
    userList = userListFromPwdFile()
    try:
        for jsonObject in userList:
            count = 0
            for params in parameterList:
                jsonParamsObject = json.loads(params)
                for key, value in jsonParamsObject.items():
                    if jsonObject[key] == value:
                        count += 1
            if count == len(parameterList) and count != 0:
                usersQueryList.append(jsonObject)
    except Exception as e:
        print(e)
        return 'Error'
    return usersQueryList

'''
<summary>Function Overloading - The groupsQuery function searches through current groupList found in /etc/groups and cross references GET request parameters to find specific groups</summary>
<returns>List of group objects</returns>
<params name='parameterList'>list of paramters passed with the GET request</params>
'''
def groupsQuery(parameterList):
    groupsQueryList = []
    groupList = groupListFromGroupFile()
    try:
        for jsonObject in groupList:
            count = 0
            for params in parameterList:
                jsonParamsObject = json.loads(params)
                for key, value in jsonParamsObject.items():
                    if jsonObject[key] == value:
                        count += 1
            if count == len(parameterList) and count != 0:
                groupsQueryList.append(jsonObject)
    except Exception as e:
        print(e)
        return 'Error'
    return groupsQueryList

'''
<summary>The usersGroupsFronUid function searches the list of users and appends the name of said objects that has the same 'gid' as the passed parameter</summary>
<returns>List of user 'names' that has the same grouping i.e. 'gid'</returns>
<params name='uid'>user id, used to identify specific users</params>
<params name='gid'>group id, used to identify grouping of users</params>
'''
def usersGroupsFromUid(uid, gid):
    userGidList = []
    userList = userListFromPwdFile()
    try:
        for jsonObject in userList:
            if (jsonObject['gid'] == str(gid)) and (jsonObject['uid'] != str(uid)):
               userGidList.append(jsonObject['name'])
    except Exception as e:
        print(e)
        return 'Error'
    return userGidList

'''
<summary>The groupListFromGroupFile function searches and retrieves the group data from /etc/group file</summary>
<returns>List objects of group information (name,gid, and members) except for the encrypted group password</returns>
'''
def groupListFromGroupFile():
    groupList = []
    try:
        with open('/etc/group') as file:
            groupList = file.read().splitlines()
        for i in range(len(groupList)):
            groupList[i] = groupList[i].split(':')
            groupList[i] = {
                'name':groupList[i][0],
                'gid':groupList[i][2],
                'members':groupList[i][3].replace(',', ' ').split()
            }
    except Exception as e:
        print(e)
        return 'Error'
    return groupList


'''
<summary>Main Function that runs the flask service application</summary>
'''
if __name__ == '__main__':
    app.run(debug=True)