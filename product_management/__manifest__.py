{
    'name': 'Product Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Product Management Module',
    'description': "This is Product Management created by Tanisha",
    'website': 'https://www.productmanagement.com',
    'depends': ['base', 'sale_management', 'website_sale', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'demo/product_category_demo.xml',
        'views/product_variant_views.xml',
        'views/shop_menu_website.xml',
        'views/user_information_website.xml',
    ],
    "assets": {
        "web.assets_frontend": [
            "product_management/static/src/js/user_info.js",
        ],
    },
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
