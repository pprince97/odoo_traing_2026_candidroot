{
    'name':'Car Rental Management',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Car Rental management summary",
    'description':"Car Rental management description",

    'website':"http://www.car.rental.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','mail','website','point_of_sale','pos_restaurant','sale_management','stock'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/vehicle_sequence.xml',
        'report/report.xml',
        'views/parent_menu.xml',
        'views/product_vehicle.xml',
        'views/vehicle_maintenance.xml',
        'views/vehicle_driver.xml',
        'views/vehicle_booking.xml',
        'views/product_inherited_view.xml',
        'views/customer.xml',
        'views/template.xml',
    ],
}