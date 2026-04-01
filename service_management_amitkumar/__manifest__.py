{
    'name': 'Service Management',
    'version': '19.0.1',
    'author': 'Amitkumar',
    'description': 'Service Management system',

    'depends': ['base', 'web', 'contacts', 'sale_management', 'website'],

    'data': [
        'security/service_security.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/category_view.xml',
        'views/services_view.xml',
        'views/service_request.xml',
        'views/templates.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'service_management_amitkumar/static/src/js/service_form.js',
        ],
    },

    'demo': [
        'demo/demo_company.xml',
    ],

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
