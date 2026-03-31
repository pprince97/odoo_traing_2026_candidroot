from odoo.http import request
from odoo import http

class ServiceRequestController(http.Controller):

    @http.route('/service-request-form', type="http", auth='user', website=True)
    def service_request_form(self):
        return request.render('service_management_tanisha.service_request_form_website')

    @http.route('/get/states', type='jsonrpc', auth='user', website=True)
    def get_states(self, country_id):
        states = request.env['res.country.state'].search([('country_id.id', '=', country_id)])
        return [{'id': s.id, 'name': s.name} for s in states]

    @http.route('/get/cities', type='jsonrpc', auth='user', website=True)
    def get_cities(self, state_id):
        cities = request.env['res.city'].search([('state_id.id', '=', state_id)])
        return [{'id': c.id, 'name': c.name} for c in cities]

    @http.route('/get/services', type='jsonrpc', auth='user', website=True)
    def get_services(self, category_id):
        services = request.env['product.template'].search([('category_id.id','=',category_id),('type','=','service')])
        return [{'id': service.id, 'name': service.name} for service in services]

    @http.route('/get/customer/details', type='jsonrpc', auth='user', website=True)
    def get_customer_details(self):
        res_user_id = self.env['res.users'].context_get()['uid']
        customer = self.env['res.partner'].search([('user_id','=',res_user_id)])
        return {'country': customer.country_id.name,'state': customer.state_id.name,'city': customer.city,'street': customer.street}

    @http.route('/get/service-request/details', type="jsonrpc", auth='user', website=True)
    def get_service_request_details(self, values):
        return request.env['service.request'].create(values)

    @http.route('/my/service-requests', type="http", auth='user', website=True)
    def tile_service_requests(self):
        res_user_id = self.env['res.users'].context_get()['uid']
        return request.render('service_management_tanisha.my_service_requests_list', {'service_requests': self.env['service.request'].search(['|',('customer_id','=',res_user_id),('company_id.owner_id','=',res_user_id)])})
