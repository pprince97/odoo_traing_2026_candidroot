{
    'name': "Owl Template",
    'description': "This module is for understanding the purpose of owl.",

    'author': "Amitkumar",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'website', 'web', 'sale_management', 'mail', 'point_of_sale', 'pos_restaurant'],

    'data': [
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/owl_data_view.xml',
        'views/pos_order_view.xml',
        'views/res_config_setting_view.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            '/owl_template/static/src/xml/add_customer_popup.xml',
            '/owl_template/static/src/js/add_customer.js',
            '/owl_template/static/src/xml/add_table_timer.xml',
            '/owl_template/static/src/js/add_table_timer.js',

            '/owl_template/static/src/js/guest_info.js',
            '/owl_template/static/src/xml/guest_outer_info.xml',
            '/owl_template/static/src/js/guest_outer_info.js',

            '/owl_template/static/src/xml/guest_inner_info.xml',
            '/owl_template/static/src/js/guest_inner_info.js',
        ],

        'web.assets_backend': [
            '/owl_template/static/src/js/main.js',
            '/owl_template/static/src/js/product_card.js',
            # '/owl_template/static/src/js/patching.js',
            '/owl_template/static/src/xml/product_card.xml',
            '/owl_template/static/src/css/product_card.css',
            # '/owl_template/static/src/views/web/fields/upload_mail_button.xml',
        ]
    },

    'installable': True,
    'application': True,
}
