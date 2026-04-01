{
    'name': 'Service Management',
    'version': '0.1',
    'summary': 'Summary of Service Management',
    'description': """
    This is description of Service Management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.service.com',
    'depends': ['base','website','sale_management','base_address_extended'],
    'data': [
        'security/service_security.xml',
        'security/ir.model.access.csv',
        'data/request_sequence.xml',
        'views/website_service.xml',
        'views/view_request.xml',
        'views/company_views.xml',
        'views/category_views.xml',
        'views/service_views.xml',
        'views/service_request_views.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
