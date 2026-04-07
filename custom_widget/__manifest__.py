{
    'name': "Cutom Widget",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'mail', 'web', 'point_of_sale','contacts' ,'pos_restaurant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/attachment_file.xml',
        'views/table_duration.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'custom_widget/static/src/xml/table_timer.xml',
            'custom_widget/static/src/xml/action_add_button_pos.xml',
            'custom_widget/static/src/xml/customer_form_dialog.xml',
            'custom_widget/static/src/js/customer_add_pos.js',
            'custom_widget/static/src/js/customer_popup.js',
            'custom_widget/static/src/js/table_timer.js',
        ],
        'web.assets_backend': [
            'custom_widget/static/src/js/button_attachment.js',
            'custom_widget/static/src/js/attachment_file.js',
            'custom_widget/static/src/js/counter.js',
            'custom_widget/static/src/xml/counter.xml',
            'custom_widget/static/src/xml/attachment_dialog.xml',
        ]
    },
    'license': 'LGPL-3',
}
