import json
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

'''
<summary>Index function that returns Hello World!; Outputs the string onto the flask landing page</summary>
<returns>Hello World!</returns>
'''
@app.route('/')
def index():
    return 'Hello World!'

'''
<summary>GET request for /users link</summary>
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
<summary>GET request for /users/query link</summary>
<returns>List of user information in readable JSON format</returns>
'''
@app.route('/users/query', methods=['GET'])
def getUsersQuery():
    userList = usersQuery()
    return jsonify(userList)


'''
<summary>userListFromPwdFile function that searches and retrieves user data from /etc/passwd file</summary>
<returns>List object of user information except for the encrypted password</returns>
'''
def userListFromPwdFile():
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
    return userList

'''
<summary>
The usersQuery function searches through current userList found in /etc/passwd and cross references GET request parameters to find specific users
Must also be tied to a GET request function call since it requires GET request arguments
</summary>
<returns>List of user objects</returns>
'''
def usersQuery():
    PARAMETERS = ['name', 'uid', 'gid', 'comment', 'home', 'shell']
    paramList = []
    usersQueryList = []
    userList = userListFromPwdFile()
    try:
        for params in PARAMETERS:
            if request.args.get(params) is not None:
                paramList.append(params)
        for jsonObject in userList:
            count = 0
            for params in paramList:
                if jsonObject[params] == request.args.get(params):
                    count += 1
            if count == len(paramList) and count != 0:
                usersQueryList.append(jsonObject)
        return usersQueryList
    except Exception:
        return 'Error'

'''
<summary>Main Function that runs the flask service application</summary>
'''
if __name__ == '__main__':
    app.run(debug=True)