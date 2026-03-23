{
    'name': 'Rental Management',
    'version': '1.0',

    'summary': 'Rental Management Sankit',
    'description': """
    this is Rental Management Sankit
    """,
    'depends': ['base', 'contacts', 'account', 'stock', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_configuration.xml',
        'views/product_serial_number.xml',
        'views/rental.xml',
        'views/customer.xml',
        'views/order.xml',
        'views/website_detail.xml',
        'views/list_rental_order.xml',
        'views/portal_template.xml',
        'views/header_template.xml',
        'wizard/rental_wizard.xml',
        'report/product_rental_report.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'rental_management_sankit/static/src/css/website_detail.css',
        ]
    },

    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
