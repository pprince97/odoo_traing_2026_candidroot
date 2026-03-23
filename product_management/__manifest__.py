{
    'name': 'Product Management',
    'version': '0.1',
    'summary': 'Summary of Product Management',
    'description': """
    This is description of Product Management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.product.com',
    'depends': ['base','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'demo/demo_category.xml',
        'views/products_view.xml'
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
