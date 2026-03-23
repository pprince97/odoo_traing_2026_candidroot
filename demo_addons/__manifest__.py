{
    'name': "Demo Addons",
    'summary': "This is the demo addon",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'application': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',

}

