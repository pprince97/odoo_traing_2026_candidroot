{
    'name': "test",

    'summary': "test",

    'description': """
test website sale
    """,

    'author': "Odoo trainee",
    'website': "https://www.website_sale.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

