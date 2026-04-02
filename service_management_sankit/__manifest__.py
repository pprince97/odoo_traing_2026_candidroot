{
    'name': 'Service Management',
    'version': '1.0',

    'summary': 'Service Management Sankit',
    'description': """
    this is Service Management Sankit
    """,
    'depends': ['base', 'contacts', 'sale', 'website', 'sale_management', 'l10n_cn_city'],
    'data': [
        'security/service_group.xml',
        'security/ir.model.access.csv',
        'views/service_company.xml',
        'views/service_category.xml',
        'views/services.xml',
        'views/service_request.xml',
        'views/template_request_service.xml',
        'views/template_for_tile.xml',
        'views/patch_of_not_negative.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'service_management_sankit/static/src/js/user_profile.js',
            'service_management_sankit/static/src/css/patch_of_not_negative.css',
        ],
        'web.assets_backend': [
            'service_management_sankit/static/src/js/patch_form.js',
        ],
    },
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
