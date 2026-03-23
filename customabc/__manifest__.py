# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Abc',
    'version': '0.1',
    'summary': 'Summary Custom ABC',
    'description': """
    This is custom module ABC
    """,
    'category': 'Uncategorized',
    'website': 'https://www.abc.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
