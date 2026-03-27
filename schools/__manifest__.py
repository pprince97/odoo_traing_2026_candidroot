{
    'name': "School Management",

    'summary': "School Management",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/classes_view.xml',
        'views/subject_view.xml',
        'views/school_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
}

