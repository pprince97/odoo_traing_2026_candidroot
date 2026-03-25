from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleRibbonFilter(WebsiteSale):

    def _shop_lookup_products(self, options, post, search, website):

        fuzzy_search_term, product_count, search_product = super()._shop_lookup_products(
            options, post, search, website
        )

        ribbon_ids = request.httprequest.args.getlist('ribbon')

        if ribbon_ids:
            try:
                ribbon_ids = [int(r) for r in ribbon_ids]

                search_product = search_product.filtered(
                    lambda p: p.website_ribbon_id.id in ribbon_ids
                )

                product_count = len(search_product)

            except:
                pass

        return fuzzy_search_term, product_count, search_product