{
    'name': "Pos Guest Info",

    'summary': "This module is for understanding the purpose of Pos Guest.",

    'description': "This module is for understanding the purpose of Pos Guest.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['point_of_sale', 'pos_restaurant'],

    'data': [
        'views/res_config_settings.xml',
        # 'views/compose_email.xml',
        # 'views/table_timer.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            # 'owl_template/static/src/xml/pos_extend.xml',
            'cr_pos_guest_info/static/src/xml/guest_info.xml',
            # 'owl_template/static/src/js/pos_extend.js',
            'cr_pos_guest_info/static/src/js/guest_info_outer.js',
            'cr_pos_guest_info/static/src/js/guest_info.js',
            'cr_pos_guest_info/static/src/js/guest_info_inner.js',
        ],

        # 'web.assets_backend': [
        #     'owl_template/static/src/js/compose_mail.js',
        #     'owl_template/static/src/js/main.js',
        #     'owl_template/static/src/js/patching.js',
        #     'owl_template/static/src/xml/product_card.xml',
        #     'owl_template/static/src/css/counter.css',
        # ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
