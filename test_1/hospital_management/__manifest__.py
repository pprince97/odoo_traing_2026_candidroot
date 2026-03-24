{
    'name':'Hospital Management',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Hospital management summary",
    'description':"Hospital management description",

    'website':"http://www.juniper.net",
    'license':'LGPL-3',
    'installable':True,

    'depends': ['base'],
    'data':[
        'security/hospital_groups_security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'demo/department_demo.xml',
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/hospital_demo.xml',
        'demo/user_demo.xml',
        'demo/admin_demo.xml',
        'data/patient_sequence.xml',
        'data/doctor_sequence.xml',
        'wizard/department_wizard.xml',
        'views/department_view.xml',
        'views/hospital_view.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
    ]
}