{
    'name': "POS Guest Info",

    'summary': "Short (1 phrase/line) summary of the POS Guest Info",

    'description': """
Long description of POS Guest Info
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'web', 'point_of_sale', 'contacts' ,'pos_restaurant' ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/view_pos_pos_form.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_guest_info/static/src/js/customer_detail.js',
            'pos_guest_info/static/src/js/customer_dialog.js',
            'pos_guest_info/static/src/js/floor_screen_patch.js',
            'pos_guest_info/static/src/js/data_service_patch.js',
            'pos_guest_info/static/src/js/payment_screen_patch.js',
            'pos_guest_info/static/src/js/pos_order_patch.js',
            'pos_guest_info/static/src/xml/guest_info.xml',
            'pos_guest_info/static/src/xml/customer_detail.xml',
        ],
    },
    'license': 'LGPL-3',
}
