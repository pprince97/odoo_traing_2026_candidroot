import xmlrpc.client

url = 'http://localhost:8080/'
db = 'new_school'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
print('--------------common-----------', common)


uid = common.login(db, username, password)
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
print('--------------models-----------', models)

x = models.execute_kw(db, uid, password, 'school_management_system.school', 'search', [[]],{'limit': 1})
print('--------------common-----------', x)
[record] = models.execute_kw(db, uid, password, 'school_management_system.school', 'read', [x])
print('--------------record all info-----------', [record])
