{
    'name': "library Management System",
    'version': "19.0.1",
    'description': "library management module ",
    'author': "sunil",

    'depends': ['base', 'contacts', 'website', 'web', 'website_sale', 'sale_management'],

    'data': [
        'security/security_access.xml',
        'security/ir.model.access.csv',
        'wizard/borrow_cancel_wizard.xml',
        'report/borrow_request_receipt_template.xml',
        'report/borrow_history_document.xml',
        'views/views.xml',
        'views/book.xml',
        'views/student.xml',
        'views/librarian.xml',
        'views/borrow_request.xml',
        # 'views/book_category.xml',
        'views/book_borrow_history_wizard.xml',
        'views/homepage_template.xml',
        'views/sale_page_inherit.xml',
        'views/profile_template.xml',
        # 'views/fleet_portal.xml',
        # 'views/res_config_settings.xml',

        'views/menu.xml',
        'views/templates.xml',
        'views/website_profile.xml',
        'views/snippets.xml',

    ],

    'demo': [
        'demo/library_demo.xml',
        'demo/website.xml',
    ],

    # 'assets': {
    #     'web.assets_frontend': [
    #         'library_management_sunil/static/src/scss/style.scss',
    #         'library_management_sunil/static/src/js/profile.js',
    #     ],
    # },

    'assets': {

        'web.assets_frontend': [
            'library_management_sunil/static/src/js/profile.js',
        ],

    },

    'license': 'LGPL-3',
    'installable': True,
    'application': True,

}
