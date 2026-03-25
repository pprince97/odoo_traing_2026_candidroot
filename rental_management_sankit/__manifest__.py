{
    'name': 'Rental Management',
    'version': '1.0',

    'summary': 'Rental Management Sankit',
    'description': """
    this is Rental Management Sankit
    """,
    'depends': ['base', 'contacts', 'account', 'fleet', 'website' ,'sale','portal'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/rental_wizard.xml',
        'views/product_configuration.xml',
        'demo/website_demo.xml',
        'views/product_serial_number.xml',
        'views/rental.xml',
        'views/customer.xml',
        'views/order.xml',
        'views/website_detail.xml',
        'views/list_rental_order.xml',
        'views/portal_template.xml',
        'views/header_template.xml',
        'views/website_template.xml',
        'views/product_template.xml',
        'views/pagination.xml',
        'views/sale_page_inherit.xml',
        'report/product_rental_report.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'rental_management_sankit/static/src/css/website_detail.css',
            # "rental_management_sankit/static/src/css/selector.css",
            # "rental_management_sankit/static/src/js/selector.js",
            # "rental_management_sankit/static/src/js/selector.js",
            # "rental_management_sankit/static/src/js/jquery.js",
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            "rental_management_sankit/static/src/js/select2.js",
        ]
    },

    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
