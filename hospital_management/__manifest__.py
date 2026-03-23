{
    'name': 'Hospital Management',
    'version': '1.4',
    'summary': 'Hospital Management System',
    'description': "This is Hospital Managent system",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','contacts','hr','mail','hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_base_views.xml',
        'views/appointment_views.xml',
        'views/partner_inherit_views.xml',
        'views/employee_inherit_views.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/admission_views.xml',
    ],

    'installable': True,
    'application': True,
    'author': 'Hospital Manager',
    'license': 'LGPL-3',
}
