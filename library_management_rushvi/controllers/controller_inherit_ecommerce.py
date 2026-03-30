from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

class ProductInheritController(WebsiteSale):

    def _shop_lookup_products(self, options, post, search, website):
        product_count, details, fuzzy_search_term = website._search_with_fuzzy("products_only", search,
                                                                               limit=None,
                                                                               order=self._get_search_order(post),
                                                                               options=options)
        search_result = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        return fuzzy_search_term, product_count, search_result



    def _shop_get_query_url_kwargs(
        self, search=None, min_price=None, max_price=None, order=None, tags=None, **kwargs
    ):
        attribute_values = request.session.get('attribute_values', [])
        my_prod = request.httprequest.args.getlist('my_prod')
        return {
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
            'order': order,
            'tags': tags,
            'attribute_values': attribute_values,
            'my_prod': my_prod,
        }

    @http.route()
    def shop(self, page=0, min_price=0.0, max_price=0.0, **post):
        selected_ids = [int(i) for i in request.httprequest.args.getlist('my_prod') if i.isdigit()]

        res = super(ProductInheritController, self).shop(page=page, min_price=min_price, max_price=max_price, **post)

        products = res.qcontext.get('products')
        if products and selected_ids:
            filtered_products = products.filtered(
                lambda p: any(id in selected_ids for id in p.custom_tag_ids.ids)
            )
            ppg = res.qcontext.get('ppg')
            ppr = res.qcontext.get('ppr')
            res.qcontext.update({
                'products': filtered_products,
                'search_count': len(filtered_products),
                'bins': TableCompute().process(filtered_products, ppg, ppr),
            })
        my_products = request.env['new.model'].search([])
        res.qcontext.update({
            'my_products': my_products,
            'selected_my_products': selected_ids,
        })

        return res
