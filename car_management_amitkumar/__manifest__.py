{
    'name': 'Hospital Management',
    'version': '19.0.1',
    'author': 'Amitkumar',
    'description': 'hospital_management_system',

    'depends': ['base','web','contacts','sale'],

    'demo': [
        # 'demo/demo_view.xml',
    ],

    'data': [
        'security/security_access.xml',
        'security/ir.model.access.csv',
        # 'security/hospital_record_rules.xml',
        'wizard/appoint_wizard_view.xml',
        'views/hospital_view.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/department_view.xml',
        'demo/demo_view.xml',
    ],

    'application': True,
    'license':'LGPL-3',

}