{
    'name':'Custom Website',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Custom Website summary",
    'description':"Custom Website description",

    'website':"http://www.website.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['website'],
    'data':[
        'views/about_us.xml',
        'views/services.xml',
        'views/custom_snippet.xml',
    ],

    'assets':{
        'web.assets_frontend': [
            'website_jui/static/src/scss/style.scss',
        ],
    },
}