{
    'name':'Service Management System',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Service management summary",
    'description':"Service management description",

    'website':"http://www.service.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','website','stock','base_address_extended','sale_management'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/main_menu.xml',
        'views/company_view.xml',
        'views/service_category_view.xml',
        'views/service_request_view.xml',
        'views/services_view.xml',
        'views/template.xml',
    ],

    'assets':{
        'web.assets_frontend': [
            'service_management_system_jui/static/src/js/service_request.js',
            'service_management_system_jui/static/src/scss/style.scss',
        ],
    },
}