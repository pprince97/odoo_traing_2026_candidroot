# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Person',
    'version': '0.1',
    'summary': 'Summary Custom person',
    'description': """
    This is custom module Person
    """,
    'category': 'Uncategorized',
    'website': 'https://www.person.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}


