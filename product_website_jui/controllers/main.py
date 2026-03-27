from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ProductTaxonomyController(WebsiteSale):

    @http.route()
    def shop(self,page=0, **post):
        response = super(ProductTaxonomyController, self).shop(**post)
        selected_taxonomy_ids = request.httprequest.args.getlist('taxonomies')
        selected_taxonomy_ids = [int(x) for x in selected_taxonomy_ids if x.isdigit()]
        print("-----------------selected_taxonomy_ids", selected_taxonomy_ids)
        taxonomy_ids = request.env['product.taxonomy'].search([])
        print("--------------taxonomy_ids", taxonomy_ids)
        domain = [('product_taxonomy_ids.id','in',selected_taxonomy_ids)]
        print(domain)

        if selected_taxonomy_ids:
            products = response.qcontext.get('products')
            if products:
                products = products.filtered(
                    lambda p: any(t.id in selected_taxonomy_ids for t in p.product_taxonomy_ids)
                )
                print(products)
                response.qcontext.update({
                    'products': products,
                })
        response.qcontext.update({
            'taxonomy_ids': taxonomy_ids,
            'taxonomies': selected_taxonomy_ids,
        })
        return response