{
    'name':'Hospital Management',
    'version':'0.1',
    'description':'Hospital management Description',
    'summary':'Hospital managemet summary',

    'author':'odoo trainee',
    'website':'http://www.hospital_management.com',
    'category':'Uncategorized',
    'license':'LGPL-3',
    'installable':True,

    'depends':['base','mail','hr'],
    'data':[
        'security/ir.model.access.csv',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
        'views/partner_view.xml',
        'views/employee_view.xml',
        'views/admission_view.xml'
    ]
}