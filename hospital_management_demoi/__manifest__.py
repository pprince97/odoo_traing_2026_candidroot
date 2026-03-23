# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital Management',
    'version': '0.1',
    'summary': 'Summary of hospital management',
    'description': """
    This is description of hospital management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.hospital.com',
    'depends': ['base','hr','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_view.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
        'views/department_view.xml',
        'views/appointment_view.xml',
        'views/bill_view.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
