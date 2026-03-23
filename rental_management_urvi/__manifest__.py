{
    'name': 'Rental Management',
    'version': '0.1',
    'summary': 'Summary of rental management',
    'description': """
    This is description of rental management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.rental.com',
    'depends': ['base', 'stock','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/rental_order_sequence.xml',
        'wizard/report_wizard.xml',
        'views/product_views.xml',
        'views/customer_views.xml',
        'views/rental_order_views.xml',
        'views/rental_report_views.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
