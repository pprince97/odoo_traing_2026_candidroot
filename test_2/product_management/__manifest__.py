{
    'name':'Product Management',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Product management summary",
    'description':"Product management description",

    'website':"http://www.product.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','mail','sale'],
    'data':[
        'security/ir.model.access.csv',
        'demo/product_category_demo.xml',
        'views/product_variant_view.xml',
        'views/material_view.xml',
        'views/surface_finish_view.xml',
        'views/uv_printing_view.xml',
        'views/color_shade_view.xml',
    ],
}