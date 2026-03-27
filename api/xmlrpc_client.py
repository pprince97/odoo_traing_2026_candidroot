import xmlrpc.client

url = 'http://localhost:8069/'
db = 'demo_library2'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}xmlrpc/2/common')
print('--------------common-----------', common)

uid = common.login(db, username, password)
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
print('--------------models-----------', models)

fields_to_read = ['id','name','barcode','state','category','description','stock','available_copies','currency','borrow_price']

x = models.execute_kw(db, uid, password, 'library.books', 'search', [[['state', '=', 'published']]])
record = models.execute_kw(db, uid, password, 'library.books', 'read', [x],{'fields': fields_to_read})
print('>>>>>>>>>>',record)
for rec in record:
    print('--------------record all info-----------', rec)
    print()

