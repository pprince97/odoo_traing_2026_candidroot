{
    'name': 'Hospital Management System',
    'version': '1.0',

    'summary': 'Hospital Management System',
    'description': """
    this is hospital management system
    """,
    'depends': ['base', 'contacts', 'mrp'],
    'data': [
        'security/res_groups_sec.xml',
        'security/ir.model.access.csv',
        'demo/hospital_demo.xml',
        'wizard/create_appointment_wizard.xml',
        'views/hospital.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment.xml',
        'report/patient_report.xml'
    ],
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
