{
    'name': "Chatter",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/attachment_wizard.xml',
        'wizard/mail_compose_message_views.xml',
    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         'owl_widget/static/src/js/address.js',
    #         'owl_widget/static/src/xml/template.xml',
    #     ],
    # },

    'installable': True,
    'application': True,
    'auto_install': False,
}
