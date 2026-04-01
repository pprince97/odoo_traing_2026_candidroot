from odoo import http, models, fields, tools, _
from odoo.http import request
from requests import session


class WebController(http.Controller):

    # User Profile Dropdown Render
    @http.route('/service-request', type='http', auth='public', website=True, methods=['GET'])
    def user_profile_menu(self):
        if request.session.uid:
            return request.render('service_management_amitkumar.service_request_form')
        else:
            return request.render('website.homepage')

    @http.route('/service-request-create', type='http', auth='public', methods=['POST'], website=True)
    def get_request_data(self, **post):

        country = post.get('country')
        state = post.get('state')
        city_name = post.get('city_name')
        city = post.get('city')


        request.env['service.request'].sudo().create({
            'companies_id': post.get('companies_id'),
            'product': post.get('product'),
            'customer_id': post.get('customer_id'),
            'category_id': post.get('category_id'),
            'date': post.get('date'),
            'country_id': post.get('country'),
            'state_id': post.get('state'),
            'city_id': post.get('city'),
            # 'city': city_name,
        })

        return request.redirect('/contactus-thank-you')


    @http.route('/get_states', type='jsonrpc', auth='public', website=True)
    def get_states(self, country_id=None, **kwargs):
        if not country_id:
            return []

        states = request.env['res.country.state'].sudo().search([
            ('country_id', '=', int(country_id))
        ])

        result = []
        for state in states:
            result.append({
                'id': state.id,
                'name': state.name
            })

        return result

    @http.route('/get_cities', type='jsonrpc', auth='public', website=True)
    def get_cities(self, state_id=None, **kwargs):
        if not state_id:
            return []

        cities = request.env['res.city'].sudo().search([
            ('state_id', '=', int(state_id))
        ])

        result = []
        for city in cities:
            result.append({
                'id': city.id,
                'name': city.name
            })

        return result


    @http.route('/get_services', type='jsonrpc', auth='public', website=True)
    def get_services(self, category_id=None, **kwargs):
        if not category_id:
            return []

        services = request.env['product.template'].sudo().search([
            ('service_category_id', '=', int(category_id))
        ])

        result = []
        for service in services:
            result.append({
                'id': service.id,
                'name': service.name
            })

        return result