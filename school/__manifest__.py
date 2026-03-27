{
    'name': 'School Management Module',
    'summary': 'School',
    'description': "",
    'author': 'My School',
    'website': 'http://www.unc.edu',
    'category': 'Uncategorized',
    'version': '1.0.1',
    'depends': ['base','sale_management',],

    'data': [
        'security/ir.model.access.csv',
        'views/students.xml',
        'views/teachers.xml',
        'views/classes.xml',
        'views/subjects.xml',
        'views/school.xml',
        'views/sale_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/admission.xml',
    ],

    'license':'LGPL-3',
}