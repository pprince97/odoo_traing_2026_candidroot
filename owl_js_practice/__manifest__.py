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

    'depends': ['base'],

    'assets':{
        'web.assets_backend': [
            'owl_js_practice/static/src/js/hello_owl.js',
            'owl_js_practice/static/src/xml/hello_owl.xml',
            'owl_js_practice/static/src/js/simple_component.js',
            'owl_js_practice/static/src/xml/simple_component.xml',
            'owl_js_practice/static/src/js/product_card.js',
            'owl_js_practice/static/src/js/product_component.js',
            'owl_js_practice/static/src/xml/product_component.xml',
            'owl_js_practice/static/src/scss/style.scss',
        ],
    },

    'data':[
        'views/menu_view.xml',
    ],
}