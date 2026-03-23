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
    'depends': ['base','contacts','hr','hr_skills','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/appointment_view.xml',
        'views/partner_view.xml',
        'views/employee_view.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/admission_view.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
