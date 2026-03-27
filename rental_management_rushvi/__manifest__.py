{
    'name': 'Rental Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Rental Management',
    'description': "",
    'author': 'ME',
    'website': '',
    'depends': ['base','stock','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/rental_order_sequence.xml',
        'report/rental_report.xml',
        'wizard/rental_history_wizard_views.xml',
        'wizard/invoice_wizard_views.xml',
        'views/rental_order_views.xml',
        'views/customer_views.xml'
    ],
    'installable': True,
    'license':'LGPL-3',
    'application': True,
}