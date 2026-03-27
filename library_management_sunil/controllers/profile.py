from odoo import http
from odoo.http import request
import base64
from odoo.exceptions import ValidationError
import mimetypes


class WebsiteProfileController(http.Controller):

    @http.route('/profile-form', type='http', auth='public', website=True)
    def profile_form(self, **kwargs):
        countries = request.env['res.country'].sudo().search([])

        error = request.session.pop('form_error', None)
        success = request.session.pop('form_success', None)
        post_data = request.session.pop('form_data', {})

        return request.render(
            'library_management_sunil.profile_form_template',
            {
                'countries': countries,
                'error': error,
                'success': success,
                'post': post_data,
            }
        )

    @http.route('/get-states', type='jsonrpc', auth='public')
    def get_states(self, country_id):
        states = request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id))])
        return [{'id': s.id, 'name': s.name} for s in states]

    @http.route('/get-cities', type='jsonrpc', auth='public')
    def get_cities(self, state_id):
        cities = request.env['res.city'].sudo().search([('state_id', '=', int(state_id))])
        return [{'id': c.id, 'name': c.name} for c in cities]

    @http.route('/submit-profile', type='http', auth='public', website=True, csrf=False)
    def submit_profile(self, **post):
        pdf_file = request.httprequest.files.get('pdf_file')
        pdf_data = None
        pdf_filename = None
        error = None

        if pdf_file:
            pdf_filename = pdf_file.filename
            file_content = pdf_file.read()

            if len(file_content) > 10 * 1024 * 1024:
                error = 'PDF file must be less than 10 MB'
            else:
                mime_type, _ = mimetypes.guess_type(pdf_filename)
                if mime_type != 'application/pdf':
                    error = 'Only PDF files are allowed'

            if not error:
                pdf_data = base64.b64encode(file_content)

        if error:
            post_text_data = {
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'country': post.get('country'),
                'state': post.get('state'),
                'city': post.get('city'),
                'city_text': post.get('city_text'),
                'address': post.get('address'),
                'zip': post.get('zip')
            }
            request.session['form_error'] = error
            request.session['form_data'] = post_text_data
            return request.redirect('/profile-form')

        request.env['website.profile'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'country_id': int(post.get('country')) if post.get('country') else False,
            'state_id': int(post.get('state')) if post.get('state') else False,
            'city': post.get('city') or post.get('city_text'),
            'address': post.get('address'),
            'zip_code': post.get('zip'),
            'pdf_file': pdf_data,
            'pdf_filename': pdf_filename,
        })

        request.session['form_success'] = 'Profile submitted successfully!'

        return request.redirect('/profile-form')
