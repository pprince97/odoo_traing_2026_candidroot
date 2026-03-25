{
    'name':'Product Website',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Product Website summary",
    'description':"Product Website description",

    'website':"http://www.website.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['website','website_sale','stock'],
    'data':[
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/template.xml',
    ],

    # 'assets':{
    #     'web.assets_frontend': [
    #         'website_jui/static/src/scss/style.scss',
    #     ],
    # },
}