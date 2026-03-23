# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'School Management',
    'version': '0.1',
    'summary': 'Summary of custom module school management ',
    'description': """
    This is discription of custom module school management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.school.com',
    'depends': ['base','sale_management','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/class_view.xml',
        'views/subject_view.xml',
        'views/school_view.xml',
        'views/admission_view.xml',
        'views/inherit_sale_order.xml',
        'views/inherit_res_partner.xml'
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}


