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
    <returns>Success if request returns a valid JSON object</returns>
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
        jsonObject = json.loads('[{"name": "root", "uid": "0", "gid": "0", "comment": "root", "home": "/root", "shell": "/bin/bash"}]')
        self.assertEqual(jsonObject, contents)

    '''
    <summary>Unit test for getUsersUid() funtion within app.py; Will only work if server is running</summary>
    <assert>Sucess if request returns a JSON object that matches the root JSON object specified within the function</assert>
    '''
    def testGetUsersUid(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users/0').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"name": "root", "uid": "0", "gid": "0", "comment": "root", "home": "/root", "shell": "/bin/bash"}]')
        self.assertEqual(jsonObject, contents)
    
    '''
    <summary>Unit test for getUsersUidGroup() function within app.py; Will only work if server is running</summary>
    <assert>Success if request returns a group JSON object that matches the root group JSONobject specified within the function</assert>
    '''
    def testGetUsersUidGroups(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/users/0/groups').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"name": "root","uid": "0","members": []}]')
        self.assertEqual(jsonObject, contents)

    '''
    <summary>Unit test for getGroups() function within app.py; Will only work if server is running</summary>
    <assert>Success if request returns a valid JSON object</assert>
    '''
    def testGetGroups(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/groups').read()
        self.assertTrue(self.isJsonObject(contents))

    '''
    <summary>Unit test for getGroupsUid() funtion within app.py; Will only work if server is running</summary>
    <assert>Sucess if request returns a JSON object that matches the root JSON object specified within the function</assert>
    '''
    def testGetGroupsUid(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/groups/0').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('{"name": "root","gid": "0","members": []}')
        self.assertEqual(jsonObject, contents)

    '''
    <summary>Unit test for getGroupsQuery() function within app.py; Will only work if server is running</summary>
    <assert>Success if request returns a JSON object that matches the root JSON object specified within the function</assert>
    '''
    def testGetGroupsQuery(self):
        contents = urllib.request.urlopen('http://127.0.0.1:5000/groups/query?members=syslog&members=miggy').read()
        contents = (contents.decode('utf-8')).strip(' \\t\\n\\r')
        contents = json.loads(contents)
        jsonObject = json.loads('[{"name": "adm","gid": "4","members":["syslog","miggy"]}]')
        self.assertEqual(jsonObject, contents)

#-------------------------------HTTP Request are above; General Functions are below-------------------------------#

    '''
    <summary>Unit test for userListFromPwdFile() function within app.py</summary>
    <asserts>assertEqual; Success if list are equal</asserts>
    <asserts>assertTrue; Success if list is not empty</asserts>
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
        queryList = {}
        queryList['blankUser'] = 'blankUser'
        usersQuery = app.usersQuery(queryList)
        self.assertEqual('Error', usersQuery)

    '''
    <summary>Unit test for groupsQuery() function within app.py</summary>
    <assert>Success if it returns an error</assert>
    '''
    def testGroupsQuery(self):
        queryList = {}
        queryList['blankUser'] = 'blankUser'
        groupsQuery = app.groupsQuery(queryList)
        self.assertEqual('Error', groupsQuery)


    '''
    <summary>Unit test for usersGroupsFromUid() function within app.py</summary>
    <assert>Success if it returns an equal assertion since root user group should not have members in its group (uid: 0, gid: 0)</assert>
    '''
    def testUsersGroupsFromUid(self):
        blankList = []
        userGidList = app.usersGroupsFromUid(0, 0)
        self.assertEqual(blankList, userGidList)

    '''
    <summary>Unit test for groupListFromGroupFile() function within app.py</summary>
    <asserts>assertEqual; Success if list are equal</asserts>
    <asserts>assertTrue; Success if list is not empty</asserts>
    '''
    def testGroupListFromGroupFile(self):
        groupListFromGroupFile = app.groupListFromGroupFile()
        self.assertTrue(len(groupListFromGroupFile) != 0)

        with open('/etc/group') as file:
            groupList = file.read().splitlines()
        for i in range(len(groupList)):
            groupList[i] = groupList[i].split(':')
            groupList[i] = {
                'name':groupList[i][0],
                'gid':groupList[i][2],
                'members':groupList[i][3].replace(',', ' ').split()
            }
        self.assertEqual(groupList, groupListFromGroupFile)

    '''
    <summary>Unit test for jsonifyParameterList() function within app.py</summary>
    <asserts>Success if list object returns a proper json object</asserts>
    '''
    def testJsonifyParameterList(self):
        parameterList = {}
        parameterList['name'] = 'root'
        jsonifyParameterList = app.jsonifyParameterList(parameterList)
        jsonObject = ['{"name": "root"}']
        self.assertEqual(jsonObject, jsonifyParameterList)

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