{
    'name':'Library Management',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Library management summary",
    'description':"Library management description",

    'website':"http://www.library.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','mail','website'],
    'data':[
        'security/library_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'data/borrow_request_sequence.xml',
        'report/borrow_request_receipt_report.xml',
        'report/borrow_history_report.xml',
        'wizard/book_borrow_history_wizard.xml',
        'wizard/borrow_request_cancel_wizard.xml',
        'views/res_config_settings.xml',
        'views/website_custom.xml',
        'views/my_account_template.xml',
        'views/website_homepage_template.xml',
        'views/header_footer_template.xml',
        'views/borrow_request_list_template.xml',
        'views/borrow_request_form_template.xml',
        'views/book_template.xml',
        'views/thank_you_template.xml',
        'views/book_list_template.xml',
        'views/borrow_request_view.xml',
        'views/books_view.xml',
        'views/borrow_request_lines_view.xml',
        'views/librarian_view.xml',
        'views/student_view.xml',
    ],

    'demo' :[
        'demo/books_demo.xml',
        'demo/student_demo.xml',
        'demo/borrow_request_demo.xml',
    ],

    'assets':{
        'web.assets_backend': [
            ('include', 'html_editor.assets_editor'),
            'library_management_jui/static/src/views/fields/book_image_history.xml',
            'library_management_jui/static/src/views/fields/book_image_history.js',
        ],
        'web.assets_frontend': [
            'library_management_jui/static/src/scss/style.scss',
        ],
    },
}