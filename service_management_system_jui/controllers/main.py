from odoo import http, _,fields
from odoo.http import request
from odoo.exceptions import AccessError
import base64

class ServiceManagementController(http.Controller):

    @http.route('/my/service/request/form', type='http', auth='user', website=True)
    def service_request_form_controller(self, **kwargs):
        return request.render('service_management_system_jui.service_request_template_form')

    @http.route('/my/service/request/list', type='http', auth='user', website=True)
    def service_request_list_controller(self, **kwargs):
        return request.render('service_management_system_jui.service_request_template_list')

    @http.route('/update/country', type='jsonrpc', auth='user', website=True)
    def details_country(self, country_key):
        states = request.env['res.country.state'].search_read([('country_id.id', '=', country_key)], ['id', 'name'])
        return {'states': states}

    @http.route('/update/state', type='jsonrpc', auth='user', website=True)
    def details_state(self, state_key):
        cities = request.env['res.city'].search_read([('state_id.id', '=', state_key)], ['id', 'name'])
        return {'cities': cities}

    @http.route('/update/category', type='jsonrpc', auth='user', website=True)
    def details_category(self, catg_key):
        services = request.env['product.template'].search_read([('category_id.id', '=', catg_key)], ['id', 'name'])
        return {'services': services}

    @http.route('/update/service', type='jsonrpc', auth='user', website=True)
    def details_services(self, service_key):
        company = request.env['product.template'].search_read([('id', '=', service_key)], ['id', 'company_id_s'])
        print(company)
        return {'company': company}

    @http.route('/service/form/submit', type='jsonrpc', auth='public', website=True)
    def details_submit(self, details_dict):
        print(details_dict)
        record = request.env['product.template'].search([('id', '=', int(details_dict['services_id']))])
        if details_dict['city_id']:
            res = request.env['res.city'].browse(int(details_dict['city_id']))
        request.env['service.request'].sudo().create({
            'date': details_dict['date'],
            'state': details_dict['state'],
            'customer_id': details_dict['customer_id'],
            'category_id': details_dict['category_id'],
            'street': details_dict['street'],
            'country_id': int(details_dict['country_id']),
            'state_id': int(details_dict['state_id']),
            'city_id': int(details_dict['city_id']) if details_dict['city_id'] else None,
            'city': details_dict['city'] if details_dict['city'] else res.name if details_dict['city_id'] else None,
            'service_id': int(details_dict['services_id']),
            'company_id_s': record.company_id_s.id
        })