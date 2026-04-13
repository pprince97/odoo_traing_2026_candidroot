from odoo import http, _,fields
from odoo.http import request
from odoo.exceptions import AccessError
from collections import OrderedDict


class ServiceManagementController(http.Controller):

    @http.route('/my/service/request/form', type='http', auth='user', website=True)
    def service_request_form_controller(self, **kwargs):
        return request.render('service_management_system_jui.service_request_template_form')

    @http.route(['/my/service/request/list','/my/service/request/list/page/<int:page>'], type='http', auth='user', website=True)
    def service_request_list_controller(self,page=0,state=None,search='', **kwargs):
        search = kwargs.get('search') or search
        domain = []
        if search:
            domain += ['|', ('request_number', 'ilike', search), ('customer_id.name', 'ilike', search)]
        state_filters = {
            'all': {'label': 'All', 'domain': []},
            'draft': {
                'label': 'Draft',
                'domain': [('state', '=', 'draft')]},
            'confirm': {
                'label': 'Confirm',
                'domain': [('state', '=', 'confirm')]},
            'cancel': {
                'label': 'Cancel',
                'domain': [('state', '=', 'cancel')]},
        }
        if not state:
            state = 'all'
        domain += state_filters[state]['domain']
        total = request.env['service.request'].search_count(domain)
        pager = request.website.pager(
            url='/my/service/request/list',
            url_args={'state': state,'search': search},
            total=total,
            page=page,
            step=3,
        )
        offset = pager['offset']
        values = request.env['service.request'].search(domain)
        values = values[offset: offset + 3]
        return request.render('service_management_system_jui.service_request_template_list',{'requests': values,'pager': pager,'default_url': '/my/service/request/list','state_filters': OrderedDict(sorted(state_filters.items())),'state': state,'search': search,'search_count': total,})

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

        if details_dict['state'] == 'confirm':
            customer = request.env['res.users'].browse(int(details_dict['customer_id']))
            service = request.env['product.template'].browse(int(details_dict['services_id']))
            order = self.env['sale.order'].with_context({'search_default_sales' : 1}).create({'partner_id': customer.partner_id.id, 'state': 'sale'})
            self.env['sale.order.line'].create({'product_id': service.id, 'price_unit': service.list_price, 'order_id': order.id})

        request.env['service.request'].sudo().create({
            'date': details_dict['date'],
            'state': details_dict['state'],
            'customer_id': int(details_dict['customer_id']),
            'category_id': int(details_dict['category_id']),
            'street': details_dict['street'],
            'country_id': int(details_dict['country_id']),
            'state_id': int(details_dict['state_id']),
            'city_id': int(details_dict['city_id']) if details_dict['city_id'] else None,
            'city': details_dict['city'] if details_dict['city'] else res.name if details_dict['city_id'] else None,
            'service_id': int(details_dict['services_id']),
            'company_id_s': record.company_id_s.id
        })