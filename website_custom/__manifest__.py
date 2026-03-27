{
    'name': 'Website Custom',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Website',
    'description': "",
    'author': 'ME',
    'website': '',
    'depends': ['base','website',],

    'assets': {
        'website.assets_frontend': [
            'static/src/css/page_1.css',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/page_1.xml',
    ],
    'installable': True,
    'license':'LGPL-3',
    'application': True,
}