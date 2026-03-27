{
    'name': "Products",
    'summary': "",
    'summary': "Productss",
    'description': "",
    'author': "Me",
    'website': "",
    'category': "Uncategorized",
    'version': '1.0',
    'depends': ['base','product'],
    'data': [
        'security/ir.model.access.csv',
        'demo/product_category_demo.xml',
        'views/product_products_views.xml'
    ],
    'demo':[
        # 'demo/product_category_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license':'LGPL-3',
}