{
    'name': 'Car Rental Sankit',
    'version': '1.0',

    'summary': 'Car Rental Sankit',
    'description': """
    this is Car Rental Sankit
    """,
    'depends': ['base', 'contacts', 'account', 'product', 'website', 'web','mail'],
    'data': [
        'security/car_rental_group.xml',
        'security/ir.model.access.csv',
        'views/car.xml',
        'views/driver.xml',
        'views/booking.xml',
        'views/booking.xml',
        'views/parts.xml',
        'views/maintenance.xml',
        'views/tile_template.xml',
        'views/template_booking.xml',
        'report/report_car_booking.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            "car_rental_sankit/static/src/js/select2.js",
            # 'library_management_sankit/static/src/views/fields/binary/file_history.js',
        ],
        'point_of_sale._assets_pos': [
            'car_rental_sankit/static/src/xml/pos_cash_inout.xml',
            'car_rental_sankit/static/src/js/cash_inout.js',
        ],
    },
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
