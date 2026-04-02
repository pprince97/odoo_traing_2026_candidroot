from odoo import http, models, fields, tools, api , _
from odoo.http import request

from odoo.addons.website.controllers.main import Website
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager



class WebsiteDetail(http.Controller):
    @http.route('/service-request/form', type='http', auth='public', website=True)
    def service_request_form(self):
        if request.session.uid:
            return request.render('service_management_sankit.service_request_form', {})
        else:
            return request.render('website.homepage', {})
        return request.render('website.contactus_thanks')

    @http.route('/service-request/create', type='http', auth='public', methods=['POST'], website=True)
    def service_request_create(self ,**post):
        request.env['service.request'].sudo().create({
            'service_date': post.get('service_date'),
            'customer_id': post.get('customer_id'),
            'country_id': post.get('country_id'),
            'state_id': post.get('state_id'),
            'city_id': post.get('city_id'),
            'company_id': post.get('company_id'),
            'service_category_id': post.get('service_category_id'),
            'service_id': post.get('service_id'),
        })
        return request.render('website.contactus_thanks')

    @http.route(['/service-request','/service-request/page/<int:page>'],  type='http', auth='public', website=True)
    def service_request(self,page=1):
        service_requests = request.env['service.request'].sudo().search([])

        total_service = service_requests.search_count([])
        step = 3
        pager = portal_pager(
            url='/service-request',
            total=total_service,
            page=page,
            step=step,
        )
        service_records = service_requests.search(
            [],
            limit=step,
            offset=pager['offset'],
            order='id asc',
        )

        # Edit
        values = {
            'service_requests': service_requests,
            'service_records': service_records,
            'page_name': 'service-request',
            'default_url': '/service-request',
            'pager': pager,
        }

        # values = {
        #     'service_requests': service_requests,
        # }
        return request.render('service_management_sankit.service_request', values)

    # For the States and City
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

    @http.route('/get_category', type='jsonrpc', auth='public', website=True)
    def get_category(self, company_id=None, **kwargs):
        if not company_id:
            return []

        categories = request.env['service.category'].sudo().search([
            ('company_id', '=', int(company_id))
        ])

        result = []
        for category in categories:
            result.append({
                'id': category.id,
                'service_name': category.service_name
            })

        return result

    @http.route('/get_services', type='jsonrpc', auth='public', website=True)
    def get_services(self, service_category_id=None, **kwargs):
        if not service_category_id:
            return []

        services = request.env['product.template'].sudo().search([
            ('service_category_id', '=', int(service_category_id))
        ])

        result = []
        for service in services:
            result.append({
                'id': service.id,
                'name': service.name
            })

        return result
