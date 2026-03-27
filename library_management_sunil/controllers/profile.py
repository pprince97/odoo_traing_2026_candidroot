from odoo import http
from odoo.http import request


class WebsiteProfileController(http.Controller):

    @http.route('/profile-form', type='http', auth='public', website=True)
    def profile_form(self, **kwargs):
        countries = request.env['res.country'].sudo().search([])
        return request.render(
            'library_management_sunil.profile_form_template',
            {
                'countries': countries
            }
        )

    @http.route('/get-states', type='jsonrpc', auth='public')
    def get_states(self, country_id):
        print("jay shree ram:", country_id)
        states = request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id))])
        data = []
        for state in states:
            data.append({'id': state.id, 'name': state.name})
        return data

    @http.route('/get-cities', type='jsonrpc', auth='public')
    def get_cities(self, state_id):
        print("kas kay mumbaikar:", state_id)
        cities = request.env['res.city'].sudo().search([('state_id', '=', int(state_id))])
        data = []
        for city in cities: data.append({'id': city.id, 'name': city.name})
        return data

    @http.route('/submit-profile', type='http', auth='public', website=True, csrf=False)
    def submit_profile(self, **post):
        request.env['website.profile'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'country_id': post.get('country'),
            'state_id': post.get('state'),
            'city': post.get('city'),
            'address': post.get('address'),
            'zip_code': post.get('zip'),
        })

        return request.redirect('/profile-form')
