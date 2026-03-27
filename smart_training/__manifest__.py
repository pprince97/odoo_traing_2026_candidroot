{
    'name': 'Smart Training',
    'version': '1.0',
    'summary':'Smart Training',
    'category': 'Uncategorized',
    'description': "",
    'author': "My Company",
    'website': "http://www.mycompany.com",

    'depends': ['base','hr','contacts',],

    'data': [
        'security/ir.model.access.csv',
        'views/employees_views.xml',
        'views/trainers_partner_views.xml',
        'views/programs_views.xml',
        'views/sessions_views.xml',
        'views/enrollments_views.xml',
        'views/certificates_views.xml',
    ],
    'license':'LGPL-3',
    'installable': True,
}