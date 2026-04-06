{
    'name': "Owl Template",

    'summary': "This module is for understanding the purpose of owl.",

    'description': "This module is for understanding the purpose of owl.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['website', 'mail', 'point_of_sale'],

    'data': [
        'views/action.xml',
        'views/compose_email.xml',
    ],

    'assets': {
         'point_of_sale._assets_pos': [
             'owl_template/static/src/xml/pos_extend.xml',
             'owl_template/static/src/js/pos_extend.js',
         ],

        'web.assets_backend': [
            'owl_template/static/src/js/compose_mail.js',
            'owl_template/static/src/js/main.js',
            'owl_template/static/src/js/patching.js',
            'owl_template/static/src/xml/product_card.xml',
            'owl_template/static/src/css/counter.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
