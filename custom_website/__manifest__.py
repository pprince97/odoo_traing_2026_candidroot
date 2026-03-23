{
    'name': 'Custom Website',
    'category': 'Website/Website',
    'summary': 'Custom Website Module',
    'website': 'https://www.customwebsite.com/',
    'description': "This is Custom Website created by Tanisha",
    'version': '1.0',
    'depends': [
        'base',
        'website',
        'web',
    ],
    'data': [
        'views/custom_website_views.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Tanisha',
    'license': 'LGPL-3',
}
