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
            products = res.qcontext.get('products')
            if products:
                filtered_products = []
                for p in products:
                    if any(id in selected_ids for id in p.product_ids.ids):
                        filtered_products.append(p)
                # filtered_products = products.filtered(lambda p: any(id in selected_ids for id in p.product_ids.ids))
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.', filtered_products)
                print('>>>>>>>>>>>>>>>>>>>>>>>>....',products.search([('product_ids','in',selected_ids)]))
                ppg = res.qcontext.get('ppg')
                ppr = res.qcontext.get('ppr')
                res.qcontext.update({
                    'products': filtered_products,
                    'search_count': len(filtered_products),
                    'bins': TableCompute().process(filtered_products, ppg, ppr),
                })
        else:
            res = super(ProductInheritController, self).shop(**post)
        my_products = request.env['my.product'].search([])
        res.qcontext.update({
            'my_products': my_products,
            'selected_my_products': selected_ids,
        })
        return res


