{
    'name': "Chatter",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'mail', 'sale'],

    'data': [
        'wizard/mail_compose_message_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'chatter_inherit/static/src/js/attachment_selector.js',
            'chatter_inherit/static/src/xml/attachment_selector.xml',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
