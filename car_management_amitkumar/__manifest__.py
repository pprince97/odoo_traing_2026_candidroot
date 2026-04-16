{
    'name': 'Car Rental Management',
    'version': '19.0.1',
    'author': 'Amitkumar',
    'description': 'Car rental management system',

    'depends': ['base','web','contacts','sale_management','website','portal','point_of_sale','pos_restaurant'],

    'data': [
        'security/car_management_security.xml',
        'security/ir.model.access.csv',
        'views/car_management_view.xml',
        'views/driver_management_view.xml',
        'views/booking_view.xml',
        'views/website_template.xml',
        'report/booking_report.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'car_management_amitkumar/static/src/app/components/navbar/cash_view.xml',
        ],
    },

    'application': True,
    'installable': True,
    'license':'LGPL-3',

}