from odoo.http import request
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale,TableCompute


class ProductController(WebsiteSale):

    @http.route()
    def shop(self, **post):
        response = super(ProductController, self).shop(**post)
        raw_ids = request.httprequest.args.getlist('functionality')
        if raw_ids:
            search_product = response.qcontext.get('search_product')
            selected_funct_ids = [int(i) for i in raw_ids if i.isdigit()]
            if search_product:
                filtered_products = search_product.filtered(
                    lambda p: any(id in selected_funct_ids for id in p.functionality_ids.ids)
                )
                ppg = response.qcontext.get('ppg')
                ppr = response.qcontext.get('ppr')
                pager = request.website.pager(
                    url="/shop",
                    total=len(filtered_products),
                    page=int(post.get('page', 1)),
                    step=ppg,
                    scope=7,
                    url_args=post
                )
                offset = pager['offset']
                products = filtered_products[offset:offset + ppg]
                variants = request.env['product.product'].sudo().browse(product._get_first_possible_variant_id() for product in products)
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
        functionalities = request.env['product.functionality'].search([])
        response.qcontext.update({
            'functionalities': functionalities,
            'raw_ids': raw_ids,
        })
        return response

    def _shop_get_query_url_kwargs(self, search, min_price, max_price, order=None, tags=None, **kwargs):
        attribute_values = request.session.get('attribute_values', [])
        raw_ids = request.httprequest.args.getlist('functionality')
        return {
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
            'order': order,
            'tags': tags,
            'attribute_values': attribute_values,
            'functionality': raw_ids,
        }


class UserInfoController(http.Controller):

    @http.route('/user-information', type="http", auth='user', website=True)
    def get_user_info_form(self):
        return request.render('product_management.user_information_form_website')

    @http.route('/get/states', type='jsonrpc', auth='user', website=True)
    def get_states(self, country_id):
        states = request.env['res.country.state'].search([('country_id.id', '=', country_id)])
        return [{'id': s.id, 'name': s.name} for s in states]

    @http.route('/get/cities', type='jsonrpc', auth='user', website=True)
    def get_cities(self, state_id):
        cities = request.env['res.city'].search([('state_id.id', '=', state_id)])
        return [{'id': c.id, 'name': c.name} for c in cities]

    @http.route('/get/user/information', type="jsonrpc", auth='user', website=True)
    def get_user_information(self, values):
        print("------------------",values)
        return request.env['res.partner'].create(values)



