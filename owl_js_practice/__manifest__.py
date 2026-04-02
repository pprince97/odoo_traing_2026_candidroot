{
    'name':'Owl Js',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Owl Js summary",
    'description':"Owl Js description",

    'website':"http://www.owl.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','web','sale_management','mail'],

    'assets':{
        'web.assets_backend': [
            'owl_js_practice/static/src/js/custom_file_dialog.js',
            'owl_js_practice/static/src/xml/custom_file_dialog.xml',
            'owl_js_practice/static/src/js/hello_owl.js',
            'owl_js_practice/static/src/xml/hello_owl.xml',
            'owl_js_practice/static/src/js/simple_component.js',
            'owl_js_practice/static/src/xml/simple_component.xml',
            'owl_js_practice/static/src/js/product_card.js',
            'owl_js_practice/static/src/js/product_component.js',
            'owl_js_practice/static/src/xml/product_component.xml',
            'owl_js_practice/static/src/scss/style.scss',
            'owl_js_practice/static/src/js/sale_order_fields.js',
            'owl_js_practice/static/src/js/notebook.js',
            'owl_js_practice/static/src/js/widget_float.js',
            'owl_js_practice/static/src/xml/widget_float.xml',
            'owl_js_practice/static/src/js/attach_widget.js',
            'owl_js_practice/static/src/xml/attach_widget.xml',
        ],
    },

    'data':[
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/custom_widget_view.xml',
        'views/mail_attachments.xml',
    ],
}