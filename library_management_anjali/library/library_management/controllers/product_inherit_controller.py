from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute

class ProductInheritController(WebsiteSale):
    def _shop_get_query_url_kwargs(
        self, search, min_price, max_price, order=None, tags=None, **kwargs
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
    def shop(self, **post):
        selected_ids = [int(i) for i in request.httprequest.args.getlist('my_prod') if i.isdigit()]
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.',selected_ids)
        if selected_ids:
            res = super(ProductInheritController, self).shop(**post)
            search_product = res.qcontext.get('search_product')
            if search_product:
                # filtered_products = []
                # for p in products:
                #     if any(id in selected_ids for id in p.product_ids.ids):
                #         filtered_products.append(p)
                filtered_products = search_product.filtered(lambda p: any(id in selected_ids for id in p.product_ids.ids))
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.', filtered_products)
                print('>>>>>>>>>>>>>>>>>>>>>>>>....',search_product.search([('product_ids','in',selected_ids)]))
                ppg = res.qcontext.get('ppg')
                ppr = res.qcontext.get('ppr')

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

                variants = request.env['product.product'].sudo().browse(
                    product._get_first_possible_variant_id() for product in products)
                variants.fetch()
                product_variants = dict(zip(products, variants))

                website = request.env['website'].get_current_website()
                new_products_prices = products._get_sales_prices(website)

                res.qcontext.update({
                    'products': products,
                    'search_product': filtered_products,
                    'search_count': len(filtered_products),
                    'bins': TableCompute().process(filtered_products, ppg, ppr),
                    'pager': pager,
                    'product_variants': product_variants,
                    'get_product_prices': lambda product: new_products_prices[product.id],
                })
        else:
            res = super(ProductInheritController, self).shop(**post)
        my_products = request.env['my.product'].search([])
        res.qcontext.update({
            'my_products': my_products,
            'selected_my_products': selected_ids,
        })
        return res


