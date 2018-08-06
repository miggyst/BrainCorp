import unittest
import app
import json
import urllib.request
from flask import jsonify

class appUnitTest(unittest.TestCase):

    '''
    <summary>Basic unit test for index function within app.py</summary>
    <asserts>assertEqual; String comparison<asserts>
    <returns>Success if return string is: Hello World!</returns>
    '''
    def testIndex(self):
        self.assertEqual(app.index(),'Hello World!')

    '''
    <summary>Unit test for getUsers() function within app.py; Will only work if server is running</summary>
    <asserts>assertTrue; Checks for json object</asserts>
    <returns>Success if request returns a JSON object</returns>
    '''
    def testGetUsers(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users').read()
        self.assertTrue(self.isJsonObject(contents))
    
    '''
    <summary>Unit test for getUsersQuery() function within app.py; Will only work if server is running</summary>
    <assert>Success if request returns a JSON object that matches the root JSON object specified within the function</assert>
    '''
    def testGetUsersQuery(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users/query?name=root').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"comment": "root","gid": "0","home": "/root","name": "root","shell": "/bin/bash","uid": "0"}]')
        self.assertTrue(jsonObject, contents)

    '''
    <summary>Unit test for getUsersUid() funtion within app.py; Will only work if server is running</summary>
    <assert>Sucess if requesr returns a JSON object that matches the root JSON object specified within the function</assert>
    '''
    def testGetUsersUid(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users/0').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"comment": "root","gid": "0","home": "/root","name": "root","shell": "/bin/bash","uid": "0"}]')
        self.assertTrue(jsonObject, contents)
    '''
    <summary></summary>
    <assert></assert>
    '''
    def testGetUsersUidGroups(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users/0/groups').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"name": "root","uid": "0","members": []}]')
        self.assertTrue(jsonObject, contents)

    '''
    <summary>Unit test for userListFromPwdFile() function within app.py</summary>
    <asserts>assertEqual; List comparison</asserts>
    <asserts>assertTrue; Checks if list is empty</asserts>
    <returns>
    assertEqual = Success if return list is the same as the list found in /etc/passwd
    assertTrue = Success if return list is NOT empty
    </returns>
    '''
    def testUserListFromPwdFile(self):
        userListFromPwdFile = app.userListFromPwdFile()
        self.assertTrue(len(userListFromPwdFile) != 0)
        
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
        self.assertEqual(userList, userListFromPwdFile)
    
    '''
    <summary>Unit test for usersQuery() function within app.py</summary>
    <assert>Success if it returns an error</assert>
    '''
    def testUsersQuery(self):
        usersQuery = app.usersQuery({'blank':'blank'})
        self.assertEqual('Error', usersQuery)

    '''
    <summary>Unit test for usersGroupsFromUid() function within app.py</summary>
    <assert>Success if it returns an equal assertion since root user group should not have members in its group (uid: 0, gid: 0)</assert>
    '''
    def testUsersGroupsFromUid(self):
        blankList = []
        userGidList = app.usersGroupsFromUid(0, 0)
        self.assertEqual(blankList, userGidList)

    '''
    <summary>Checks whether or not an object is a JSON object</summary>
    <param name = 'jsonObject'>jsonObject is top be checked whether or not it is of a JSON format</param>
    <returns>True if jsonObject is truly a jsonObject, else False</returns>
    '''
    def isJsonObject(self, jsonObject):
        try:
            jsonOjectValidate = json.loads(jsonObject)
        except ValueError:
            return False
        return True

'''
<summary>Main Function that runs unit tests</summary>
'''
if __name__ == '__main__':
    unittest.main()