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
        return jsonify(userList[0])#jsonify(userList)

'''
<summary>GET request for /users/<uid>/groups web link</summary>
<returns>
User information with a list of tied groups, dependent on UID;
Will return 'Error' if wrong UID is passed</returns>
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
<summary>userListFromPwdFile function that searches and retrieves user data from /etc/passwd file</summary>
<returns>List object of user information except for the encrypted password</returns>
'''
def userListFromPwdFile():
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
    except Exception:
        return 'Error'
    return userList

'''
<summary>The usersQuery function searches through current userList found in /etc/passwd and cross references GET request parameters to find specific users</summary>
<returns>List of user objects</returns>
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
    except Exception:
        return 'Error'
    return usersQueryList

'''
<summary></summary>
<returns></returns>
'''
def usersGroupsFromUid(uid, gid):
    userGidList = []
    userList = userListFromPwdFile()
    try:
        for jsonObject in userList:
            if (jsonObject['gid'] == str(gid)) and (jsonObject['uid'] != str(uid)):
               userGidList.append(jsonObject['name'])
    except Exception:
        return 'Error'
    return userGidList

'''
<summary>Main Function that runs the flask service application</summary>
'''
if __name__ == '__main__':
    app.run(debug=True)