from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http, _,fields
from odoo.http import request
from odoo.addons import website
from odoo.fields import Command, Domain
import base64

class ProductAttributeController(WebsiteSale):
    def product_attributes(self):
        website_domain = website.website_domain()
        filter_by_taxonomy_enabled = website.is_view_active('product_website_jui.product_taxonomy_template')
        ProductTaxonomy = request.env['product.taxonomy']
        if filter_by_taxonomy_enabled and search_product:
            all_tags = ProductTaxonomy.search_fetch(Domain.AND([
                Domain('visible_to_customers', '=', True),
                Domain.OR([
                    Domain('product_template_ids.is_published', '=', True),
                    Domain('product_ids.is_published', '=', True),
                ]),
                website_domain,
            ]))
        else:
            all_tags = ProductTaxonomy