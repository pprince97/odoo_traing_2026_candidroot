
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Test',
    'category': 'Uncategorized',
    'summary': 'Website Test',
    'description' : 'Website Test',
    'website': 'https://www.google.com',
    'version': '1.0',
    'depends': ['website'],
    'installable': True,
    'data': [
        'views/website_menus.xml'
    ],
    'application': True,
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
