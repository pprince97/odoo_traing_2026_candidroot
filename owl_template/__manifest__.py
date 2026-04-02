{
    'name': "Owl Template",

    'summary': "This module is for understanding the purpose of owl.",

    'description': "This module is for understanding the purpose of owl.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base','web','mail'],

    'data': [
        'views/action.xml',
        'views/button_link.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'owl_template/static/src/js/counter.js',
            'owl_template/static/src/js/link_button.js',
            'owl_template/static/src/js/custom_dialog.js',
            'owl_template/static/src/xml/custom_dialog.xml',
            'owl_template/static/src/xml/counter.xml',
            'owl_template/static/src/xml/link_button.xml',
            'owl_template/static/src/css/counter.css',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
