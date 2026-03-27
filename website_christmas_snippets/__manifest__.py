{
    "name": "Christmas Snippets",
    "description": """
Christmas Snippets for Odoo Website
===================================

Transform your Odoo website for the holiday season with a collection of festive, animated snippets.

Features:
---------
* **Falling Snow**: Add a gentle snow effect to any page.
* **Santa & Reindeer**: Animated characters to bring joy to visitors.
* **Festive Banners**: Ready-to-use holiday headers.
* **Decorations**: Ornaments, lights, and trees to decorate your content.
* **Fully Responsive**: Works perfectly on mobile and desktop.

Search Keywords:
----------------
christmas, holiday, new year, festive, snippets, website theme, snow effect, animation, decorations, santa, winter, seasonal, website builder, building blocks, design.
    """,
    "category": "Website",
    "version": "19.0.1.0.0",
    "summary": "Festive Christmas snippets for Odoo Website",
    "author": "Daksh Solutions & Services",
    "website": "https://dakshsoft.in",
    "license": "LGPL-3",
    "images": ["static/description/banner.png"],
    "depends": ["website"],
    "data": [
        "views/snippets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_christmas_snippets/static/src/scss/_variables.scss",
            "website_christmas_snippets/static/src/scss/theme_overrides.scss",
            "website_christmas_snippets/static/src/scss/theme_full.scss",
            "website_christmas_snippets/static/src/js/theme.js",
        ],
    },
    "price": 0,
    "currency": "EUR",
    "application": True,
    "installable": True,
}
