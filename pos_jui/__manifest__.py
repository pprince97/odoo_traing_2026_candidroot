{
    'name':'Point Of Sale New',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Point Of Sale New summary",
    'description':"Point Of Sale New description",

    'website':"http://www.pos.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','point_of_sale','pos_restaurant'],
    'data':[
        "security/ir.model.access.csv",
       'views/order_view.xml',
       'views/res_config_settings.xml',
    ],

    'assets':{
        'point_of_sale._assets_pos': ['pos_jui/static/src/**/*'],
    },
}