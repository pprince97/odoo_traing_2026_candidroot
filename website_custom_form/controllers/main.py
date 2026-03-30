from odoo import http
from odoo.http import request
import base64

class WebsiteLocation(http.Controller):

    @http.route('/city/form/', type='http', auth='public', methods=['POST'], website=True)
    def get_form_data(self, **post):

        country = post.get('country') or False
        state = post.get('state') or False
        city_name = post.get('city_name') or False
        city = post.get('city') or False
        file = request.httprequest.files.get('document')

        filename = file.filename
        file_content = file.read()
        file_size = len(file_content)

        if not filename.lower().endswith('.pdf'):
            return "Only PDF files are allowed"

        if file_size > 10 * 1024 * 1024:
            return "File size must be less than 10MB"

        encoded_file = base64.b64encode(file_content)

        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'country_id': int(country),
            'state_id': int(state),
            'city_id': int(city) or False,
            'city': city_name,
            'file_pdf': encoded_file,
            'file_pdf_name': filename,
        })

        return request.redirect('/thank-you')

    @http.route('/thank-you', type='http', auth='public', website=True)
    def thank_you(self, **kwargs):

        return request.render('website_custom_form.thank_you')


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