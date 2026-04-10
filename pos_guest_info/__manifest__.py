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
    'depends': ['base', 'sale', 'web', 'point_of_sale','contacts' ,'pos_restaurant' ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/customer_info.xml',
        'views/guest_detail.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # 'custom_widget/static/src/xml/table_timer.xml',
            # 'custom_widget/static/src/xml/action_add_button_pos.xml',
            # 'custom_widget/static/src/xml/customer_form_dialog.xml',
            'pos_guest_info/static/src/js/customer_detail.js',
            'pos_guest_info/static/src/js/guest_info.js',
            'pos_guest_info/static/src/js/table_click.js',
            'pos_guest_info/static/src/js/pos_store.js',
            'pos_guest_info/static/src/xml/guest_info.xml',
            'pos_guest_info/static/src/xml/customer_detail.xml',
            # 'custom_widget/static/src/js/customer_popup.js',
            # 'custom_widget/static/src/js/table_timer.js',
        ],
        'web.assets_backend': [
            # 'custom_widget/static/src/js/button_attachment.js',
            # 'custom_widget/static/src/js/attachment_file.js',
            # 'custom_widget/static/src/js/counter.js',
            # 'custom_widget/static/src/xml/counter.xml',
            # 'custom_widget/static/src/xml/attachment_dialog.xml',
        ]
    },
    'license': 'LGPL-3',
}
