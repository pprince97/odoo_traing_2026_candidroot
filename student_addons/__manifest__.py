{
    'name': 'Student Data',
    'summary': 'This is student addon',
    'category': 'Hidden',
    'version': '1.0',
    'description': """
Long description of module's purpose
""",
    'depends': ['base'],
    'application': True,
    'website': "https://www.yourcompany.com",
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
    ],

    'author': 'My School',
    'license': 'LGPL-3',
}
