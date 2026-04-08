{
    'name': "Owl Template",

    'summary': "This module is for understanding the purpose of owl.",

    'description': "This module is for understanding the purpose of owl.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'mail', 'point_of_sale', 'pos_restaurant'],

    'data': [
        'views/pos_order_inherit.xml',
        'views/action.xml',
        'views/button_link.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'owl_template_u/static/src/app/components/screens/product_screen/control_buttons/control_buttons.xml',
            'owl_template_u/static/src/app/components/screens/product_screen/control_buttons/control_buttons.js',
            'owl_template_u/static/src/app/components/popup/customer_popup.xml',
            'owl_template_u/static/src/app/components/popup/timer.xml',
            'owl_template_u/static/src/app/components/popup/customer_popup.js',
            'owl_template_u/static/src/app/components/popup/timer.js',
        ],
        'web.assets_backend': [
            'owl_template_u/static/src/js/counter.js',
            'owl_template_u/static/src/js/link_button.js',
            'owl_template_u/static/src/js/custom_dialog.js',
            'owl_template_u/static/src/xml/custom_dialog.xml',
            'owl_template_u/static/src/xml/counter.xml',
            'owl_template_u/static/src/xml/link_button.xml',
            'owl_template_u/static/src/css/counter.css',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
