{
    'name': "Library Management Smit",

    'summary': "This module is for library management.",

    'description': "This module is for library management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'website'],

    'demo': [
        'demo/book_demo.xml',
        'demo/students_demo.xml',
        'demo/borrow_records_demo.xml',
    ],

    'data': [
        'security/security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'wizard/book_borrow_history_wizard.xml',
        'wizard/cancellation_wizard.xml',
        'report/book_history_report.xml',
        'report/report_borrow_request.xml',
        'views/template.xml',
        'views/librarian_view.xml',
        'views/borrow_request_view.xml',
        'views/student_view.xml',
        'views/book_views.xml',
        'views/book_image_history_views.xml',
        'views/menu_views.xml',
        'data/borrow_seq.xml',
        'demo/book_demo.xml',
        'demo/students_demo.xml',
        'demo/borrow_records_demo.xml',
        'views/res_config_settings.xml',
    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         'library_management_smit/static/src/js/custom_image_field.js',
    #         'library_management_smit/static/src/xml/custom_image_field.xml',
    #     ],
    # },

    'installable': True,
    'application': True,
    'auto_install': False,
}
