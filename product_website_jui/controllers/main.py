from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

class ProductTaxonomyController(WebsiteSale):
    def _shop_get_query_url_kwargs(self, search, min_price, max_price, order=None, tags=None, **kwargs):
        attribute_values = request.session.get('attribute_values', [])
        my_product = request.httprequest.args.getlist('taxonomies')
        return {
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
            'order': order,
            'tags': tags,
            'attribute_values': attribute_values,
            'taxonomies': my_product,
        }

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        selected_taxonomy = request.httprequest.args.getlist('taxonomies')
        response = super(ProductTaxonomyController, self).shop(page=page, category=category, search=search,
                                                               ppg=ppg, **post)

        if selected_taxonomy:
            selected_taxonomy_ids = [int(x) for x in selected_taxonomy if x.isdigit()]
            search_product = response.qcontext.get('search_product')
            if search_product:
                filtered_products = search_product.filtered(
                    lambda p: any(id in selected_taxonomy_ids for id in p.product_taxonomy_ids.ids)
                )

                ppg = response.qcontext.get('ppg')
                ppr = response.qcontext.get('ppr')
                pager = request.website.pager(
                    url="/shop",
                    total=len(filtered_products),
                    page=int(post.get('page', 1)),
                    step=ppg,
                    scope=7,
                    url_args=post  # Keeps the 'applications' in the URL
                )

                offset = pager['offset']
                products = filtered_products[offset:offset + ppg]

                variants = request.env['product.product'].sudo().browse(
                    product._get_first_possible_variant_id() for product in products)
                variants.fetch()
                product_variants = dict(zip(products, variants))

                website = request.env['website'].get_current_website()
                new_products_prices = products._get_sales_prices(website)

                response.qcontext.update({
                    'products': products,
                    'bins': TableCompute().process(products, ppg, ppr),
                    'search_count': len(filtered_products),
                    'search_product': filtered_products,
                    'pager': pager,
                    'product_variants': product_variants,
                    'get_product_prices': lambda product: new_products_prices[product.id],
                })


        taxonomies = request.env['product.taxonomy'].sudo().search([])
        response.qcontext['taxonomies'] = taxonomies
        return response