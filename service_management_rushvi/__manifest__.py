{
    'name': "Service Management",
    'summary': "Service Management",
    'description': "",
    'author': "Me",
    'website': "",
    'category': "Uncategorized",
    'version': '1.0',
    'depends': ['base','account','sale','portal','web','product','website'],
    'assets': {
        'web.assets_frontend': [
            'web.core',
            'service_management_rushvi/static/src/js/main.js',
        ],
        'web.assets_backend': [
                    # 'service_management_rushvi/static/src/fields/history_field/*.js',
                    # 'service_management_rushvi/static/src/fields/history_field/*.xml',
                ],
    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/service_request_sequence.xml',
        'views/views_service_company.xml',
        'views/views_service_category.xml',
        'views/views_services.xml',
        'views/views_service_requests.xml',
        'views/request_service_tile.xml',
        ],
    'installable': True,
    'application': True,
    'license':'LGPL-3',
}