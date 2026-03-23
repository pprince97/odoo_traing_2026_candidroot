{
    'name': 'Gym Management',
    'version': '1.0',
    'summary': 'Gym Management System',
    'website': 'https://www.gymmanagement.com',
    'category': 'Hidden',
    'description': "This is the description of Gym Management System",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_base_views.xml',
        'views/member_views.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'GYM',
    'license': 'LGPL-3',
}
