{
    'name':'Practice',
    'version':'0.1',
    'summary':'practice summary',
    'description':'practice description',

    'author':'odoo trainee',
    'website':"https://www.practice.com",
    'license':'LGPL-3',
    'installable':True,

    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/',
    ]
}