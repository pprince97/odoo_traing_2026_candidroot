{
    'name': 'Hospital Management',
    'version': '0.1',
    'summary': 'Summary of hospital management',
    'description': """
    This is description of hospital management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.hospital.com',
    'demo': [
        # 'demo/hospital_demo.xml'
    ],
    'depends': ['base', 'contacts'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'wizards/department_wizard_view.xml',
        'views/hospital_views.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/department_views.xml',
        'demo/department_demo.xml',
        'demo/hospital_demo.xml',
        'demo/appointment_demo.xml',
        'demo/user_demo.xml',
        'data/doctor_data.xml',
        'data/patient_data.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
