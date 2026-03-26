from odoo.http import request
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale,TableCompute


class ProductController(WebsiteSale):

    @http.route()
    def shop(self,funct='',**post):
        raw_ids = request.httprequest.args.getlist('functionality')
        response = super(ProductController, self).shop(**post)
        if raw_ids:
            selected_funct_ids = [int(i) for i in raw_ids if i.isdigit()]
            print("---------selected_funct_ids", selected_funct_ids)
            if selected_funct_ids:
                filtered_products = []
                products = response.qcontext.get('products')
                print("----------products-----------",products)
                for p in products:
                    for pro_func in p.functionality_ids.ids:
                        if pro_func in selected_funct_ids:
                            filtered_products.append(p)
                print("------------filtered_products-----------",filtered_products)
        functionalities = request.env['product.functionality'].search([])
        response.qcontext.update({
            'functionalities': functionalities,
        })
        return response
