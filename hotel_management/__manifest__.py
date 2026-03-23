# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hotel Management',
    'version': '0.1',
    'summary': 'Summary of hotel management',
    'description': """
    This is description of hotel management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.hotel.com',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hotel_view.xml',
        'views/room_view.xml',
        'views/guest_view.xml',
        'views/booking_view.xml',
        'views/service_view.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
