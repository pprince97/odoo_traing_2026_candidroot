
{
    'name': 'POS Custom',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'This module is for understanding the purpose of POS',
    'description': "This module is for understanding the purpose of POS",
    'website': 'https://www.poscustom.com',
    'depends': ['base', 'pos_restaurant'],
    'data': [
        'security/ir.model.access.csv',
        'views/guest_details_res_config.xml',
        'views/guest_details_views.xml',
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_custom_tanisha/static/src/app/components/screens/floor_screen/guest_details_dialog.js",
            "pos_custom_tanisha/static/src/app/components/screens/floor_screen/guest_details_dialog.xml",
            "pos_custom_tanisha/static/src/app/components/screens/floor_screen/pos_floor_screen.js",
            "pos_custom_tanisha/static/src/app/components/screens/floor_screen/pos_floor_screen.xml",
            "pos_custom_tanisha/static/src/app/components/screens/product_screen/control_buttons/pos_control_button.xml",

        ],
    },
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
