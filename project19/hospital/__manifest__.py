{
    'name':'Hospital',
    'version':'0.1',
    'description':'Hospital management Description',
    'summary':'Hospital managemet summary',

    'author':'odoo trainee',
    'website':'http://www.hospital_management.com',
    'category':'Uncategorized',
    'license':'LGPL-3',
    'installable':True,

    'depends':['base','mail','hr','account'],
    'data':[
        'security/ir.model.access.csv',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/patients.xml',
        'views/rooms.xml',
        'views/bill.xml'
    ]
}