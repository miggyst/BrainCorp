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
<summary>Main Function that runs the flask service application</summary>
'''
if __name__ == '__main__':
    app.run(debug=True)