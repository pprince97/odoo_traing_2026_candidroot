{
    'name':'Rental Management System',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Rental management summary",
    'description':"Rental management description",

    'website':"http://www.rental.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','mail','sale','stock'],
    'data':[
        'security/ir.model.access.csv',
        'views/rental_management_system_view.xml',
        'views/product_view.xml',
        'views/customer_view.xml',
        'views/rental_order_lines.xml',
        'views/rental_order.xml',
    ],
}