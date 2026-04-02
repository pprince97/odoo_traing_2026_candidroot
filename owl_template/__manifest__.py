{
    'name': "Owl Template",
    'description': "This module is for understanding the purpose of owl.",

    'author': "Amitkumar",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'website', 'web', 'sale_management', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/owl_data_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            '/owl_template/static/src/js/main.js',
            '/owl_template/static/src/js/product_card.js',
            '/owl_template/static/src/js/patching.js',
            '/owl_template/static/src/xml/product_card.xml',
            '/owl_template/static/src/css/product_card.css',
            # '/owl_template/static/src/views/web/fields/upload_mail_button.xml',
        ]
    },

    'installable': True,
    'application': True,
}
