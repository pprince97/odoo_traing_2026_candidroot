{
    'name': 'Library Management',
    'version': '0.1',
    'summary': 'Summary of library management',
    'description': """
    This is description of library management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.library.com',
    'depends': ['base', 'mail', 'website'],
    'assets': {
        'web.assets_backend': [
            'library_management_urvi/static/src/fields/history_field/*.xml',
            'library_management_urvi/static/src/fields/history_field/*.js',
        ]
    },
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/borrow_sequence.xml',
        'report/receipt_report.xml',
        'report/history_report.xml',
        'wizard/borrow_history_wizard.xml',
        'wizard/cancel_wizard.xml',
        'views/website_different.xml',
        'views/website_menus.xml',
        'views/website_book.xml',
        'views/website_borrow.xml',
        'views/website_student.xml',
        'views/website_reporting.xml',
        'views/config_parameter_library.xml',
        'views/borrow_request_views.xml',
        'views/book_views.xml',
        'views/librarian_views.xml',
        'views/student_views.xml',
        'views/reporting_views.xml',
    ],
    'demo': [
        'demo/book_demo.xml',
        'demo/student_demo.xml',
        'demo/borrow_request_demo.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
