{
    'name': 'Library Management',
    'version': '19.0.0.1',
    'summary': 'Library Management',
    'category': 'uncategorized',
    'summary': 'Library Management',
    'description': 'Library Management',
    'author': 'Man Patel',
    'depends': [
        'base', 'contacts', 'mail', 'website',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'demo/demo.xml',
        'data/library_sequence.xml',
        'report/borrow_request_receipt.xml',
        'report/book_borrow_history_report.xml',
        'wizards/book_borrow_history.xml',
        'wizards/cancellation_request.xml',
        'views/book_history.xml',
        'views/website_library.xml',
        # 'views/multi_website_library.xml',
        'views/res_config_setting.xml',
        'views/library_student.xml',
        'views/library_librarian.xml',
        'views/library_borrow_request.xml',
        'views/library_borrow_request_line.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'library_management_man/static/src/css/website_library.css'
        ],
    },

    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'license': 'LGPL-3',
    'installable': True,
    'application': True,

}
