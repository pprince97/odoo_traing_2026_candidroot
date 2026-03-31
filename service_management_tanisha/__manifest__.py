{
    'name': 'Service Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Service Management Module',
    'description': "This is Service Management created by Tanisha",
    'website': 'https://www.servicemanagement.com',
    'depends': ['base','stock','sale_management','website','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/service_request_seq.xml',
        'views/company_backend_views.xml',
        'views/category_backend_views.xml',
        'views/services_backend_views.xml',
        'views/request_backend_views.xml',
        'views/service_request_frontend_views.xml',
    ],
    "assets": {
        "web.assets_frontend": [
            "service_management_tanisha/static/src/js/service_request.js",
        ],
    },
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
