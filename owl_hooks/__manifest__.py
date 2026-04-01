{
    'name': 'owl hooks',
    'version': '0.1',
    'summary': 'Summary of owl hooks',
    'description': """
    This is description of owl hooks
    """,
    'category': 'Uncategorized',
    'website': 'https://www.owl.com',
    'depends': ['base','web'],
    'data': [
        'views/hook_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'owl_hooks/static/src/js/counter.js',
            'owl_hooks/static/src/xml/counter_template.xml',
        ],
    },
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
