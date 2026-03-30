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
        if details_dict['city_id']:
            res = request.env['res.city'].browse(int(details_dict['city_id']))
        request.env['res.partner'].sudo().create({
            'name': details_dict['name'],
            'email': details_dict['email'],
            'phone': details_dict['phone'],
            'zip': details_dict['zip'],
            'country_id': int(details_dict['country']),
            'state_id': int(details_dict['state']),
            'city_id': int(details_dict['city_id']) if details_dict['city_id'] else None,
            'city': details_dict['city'] if details_dict['city'] else res.name if details_dict['city_id'] else None,
            'image_1920': details_dict['img'] if details_dict['img'] else False,
            'doc_name': details_dict['file_name'],
            'document': details_dict['document'] if details_dict['document'] else False,
        })

    @http.route('/update', type='http', auth='public', website=True)
    def details(self):
        return request.render("product_website_jui.customer_details_template")