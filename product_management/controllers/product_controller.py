from odoo.http import request
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale,TableCompute


class ProductController(WebsiteSale):

    @http.route()
    def shop(self,**post):
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



