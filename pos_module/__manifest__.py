{
    'name': 'POS Management',
    'version': '19.0.0.1',
    'summary': 'POS Management',
    'category': 'uncategorized',
    'description': 'POS Management',
    'author': 'Aayush',
    'depends': ['base', 'point_of_sale'],

    'data': [
        'security/ir.model.access.csv',

    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_module/static/src/**/*',
        ],
    },
        'license': 'LGPL-3',
        'installable': True,
        'application': True,

}
