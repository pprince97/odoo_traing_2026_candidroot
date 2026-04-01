{
    'name': "Owl Shoping Template",

    'summary': "This module is for understanding the purpose of owl.",

    'description': "This module is for understanding the purpose of owl.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['website'],

    'data': [
        'views/action.xml',
    ],

    'assets': {
        'web.assets_backend': [
            # 'owl_shoping_cart/static/src/js/custom_popup.js',
            'owl_shoping_cart/static/src/js/shopping_cart.js',
            'owl_shoping_cart/static/src/js/action_swiper.js',
            'owl_shoping_cart/static/src/xml/shopping_cart.xml',
            'owl_shoping_cart/static/src/css/shoping_cart.css',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
