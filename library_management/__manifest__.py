# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Library Management',
    'version': '0.1',
    'summary': 'Library Management Summary',
    'description': """
This is the custom module for library management.
    """,
    'category': 'Uncategorized',
    'website': 'https://www.library.com',
    'depends': [
        'base',
        'contacts',
        'sale',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/library_view.xml',
        'views/user_view.xml',
        'views/author_view.xml',
        'views/rent_view.xml',
    ],
    'application' : True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
