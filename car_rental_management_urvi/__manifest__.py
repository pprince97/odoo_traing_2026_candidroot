{
    'name': 'Car Rental Management',
    'version': '0.1',
    'summary': 'Summary of car rental management',
    'description': """
    This is description of car rental management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.car_rental.com',
    'depends': ['base', 'mail', 'website', 'sale_management', 'contacts', 'point_of_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'data/sequence_data.xml',
        'report/booking_report.xml',
        'views/vehicle_views.xml',
        'views/driver_views.xml',
        'views/booking_views.xml',
        'views/maintenance_views.xml',
        'views/website_booking.xml',

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'car_rental_management_urvi/static/src/app/components/navbar/detail_navbar.xml',
            'car_rental_management_urvi/static/src/app/components/navbar/detail_navbar.js',
        ]},
    # 'assets': {
    #     'point_of_sale.assets': [
    #         'car_rental_management_urvi/static/src/app/components/navbar/detail_navbar.xml',
    #     ],
    # },

    # 'demo': [
    #     'demo/book_demo.xml',
    #     'demo/student_demo.xml',
    #     'demo/borrow_request_demo.xml',
    # ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
