{
    'name': 'Product Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Product Management Module',
    'description': "This is Product Management created by Tanisha",
    'website': 'https://www.productmanagement.com',
    'depends': ['base','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'demo/product_category_demo.xml',
        'views/product_variant_views.xml',
        'views/shop_menu_website.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
