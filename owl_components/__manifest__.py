{
    'name': 'Owl Components',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'This module is for understanding the purpose of owl',
    'description': "This module is for understanding the purpose of owl",
    'website': 'https://www.owlcomponents.com',
    'depends': ['base','web','mail'],
    'data': [
        'views/counter_action_views.xml',
        'views/attach_button_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "owl_components/static/src/js/counter.js",
            "owl_components/static/src/xml/counter.xml",
            "owl_components/static/src/js/attach_button.js",
            "owl_components/static/src/xml/attach_button_template.xml",

        ],
    },
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
