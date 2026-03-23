{
    'name': 'Products',
    'category': 'Hidden',
    'version': '1.0',
    'summary': 'Product Addon',
    'description': "This is a product addon with all the necessary details of the product",
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Candidroot',
    'license': 'LGPL-3',
}
