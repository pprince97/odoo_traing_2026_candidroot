{
    'name': "Owl Understanding",

    'summary': "This module made to understanding owl.",

    'description': "This module made to understanding owl.",

    'author': "Aayush",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'web', 'website'],

    'data': [
        'security/ir.model.access.csv',
        'static/src/xml/menu.xml',
        'views/score.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'owl_understand_module/static/src/js/app.js',
            'owl_understand_module/static/src/js/patch.js',
            'owl_understand_module/static/src/xml/app.xml',
            'owl_understand_module/static/src/css/style.css',
        ],
    },

    'license': 'LGPL-3',

    'installable': True,
    'application': True,
}
