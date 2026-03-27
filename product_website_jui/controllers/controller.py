from odoo import http
from odoo.http import request
import base64

class ProductWebsiteController(http.Controller):
    @http.route('/update/country', type='jsonrpc', auth='public', website=True)
    def details_country(self,country_key):
        countries = request.env['res.country.state'].search_read([('country_id.id','=',country_key)],['id', 'name'])
        return {'countries': countries}

    @http.route('/update/city', type='jsonrpc', auth='public', website=True)
    def details_city(self, city_key):
        cities = request.env['res.city'].search_read([('state_id.id', '=', city_key)],['id', 'name'])
        return {'cities': cities}

    @http.route('/details/submit', type='jsonrpc', auth='public', website=True)
    def details_submit(self, details_dict):
        print(details_dict)
        request.env['res.partner'].sudo().create({
            'name': details_dict['name'],
            'email': details_dict['email'],
            'phone': details_dict['phone'],
            'zip': details_dict['zip'],
            'country_id': int(details_dict['country']),
            'state_id': int(details_dict['state']),
            'city': details_dict['city'],
            'image_1920': details_dict['img'] if details_dict['img'] else False,
        })

    @http.route('/update', type='http', auth='public', website=True)
    def details(self):
        return request.render("product_website_jui.customer_details_template")