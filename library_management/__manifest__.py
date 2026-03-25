{
    'name': "Library Management",
    'summary': "This is a Library Management module",
    'description': """
    This is module made in v19 odoo. This module implements library management.
    """,

    'author': "Admin",
    'version': '0.1',
    'depends': ['base', 'mail','website'],

    'data': [
        'Demo/demo_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/cancellation_wizard_view.xml',
        'wizard/report_history_wizard.xml',
        'views/books.xml',
        'views/barcode_sequence.xml',
        'views/borrow_request.xml',
        'views/serial_number_sequence.xml',
        'views/librarian.xml',
        'views/student.xml',
        'views/borrow_request_lines.xml',
        'views/res_config_settings.xml',
        'views/library_website.xml',
        'views/library_website_menu.xml',
        'views/templates.xml',
        # 'report/report_wizard.xml',
    ],
    # 'demo': [
    #     'demo/account_demo.xml',
    # ],

    'license': 'LGPL-3',

    'installable': True,
    'application': True,
}
