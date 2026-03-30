from odoo import http
from odoo.http import request
# import base64

class PartnerFormController(http.Controller):

    @http.route('/get_states', type='jsonrpc', auth='public', website=True)
    def get_states(self, country_id):
        states = request.env['res.country.state'].sudo().search([
            ('country_id', '=', int(country_id))
        ])
        return [{'id': s.id, 'name': s.name} for s in states]

    @http.route('/get_cities', type='jsonrpc', auth='public', website=True)
    def get_cities(self, state_id):
        cities = request.env['res.city'].sudo().search([
            ('state_id', '=', int(state_id))
        ])
        return [{'id': c.id, 'name': c.name} for c in cities]

    @http.route('/librarians/register-form', type='http', auth='public', website=True)
    def librarian_form_page(self, **kwargs):
        countries = request.env['res.country'].search([])
        return request.render('library_management_rushvi.template_librarian_form', {
            'countries': countries
        })

    @http.route('/librarians/create', type='jsonrpc', auth='user', website=True)
    def create_librarian(self, params):
        params['is_librarian'] = True
        try:
            request.env['res.partner'].sudo().create(params)
            return {
                'redirection_url': '/librarians/',
                'success': True,
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    # @http.route('/librarians/create', type='http', methods=['POST'],auth='user', website=True)
    # def create_librarian(self, **post):
    #     pdf_base64 = False
    #     resume_base64 = post.get('resume')
    #     if resume_base64:
    #         pdf_base64 = base64.b64encode(resume_base64.read()).decode('utf-8')
    #     vals = {
    #         'name': post.get('name'),
    #         'email': post.get('email'),
    #         'phone': post.get('phone'),
    #         'country_id': int(post.get('country_id')) if post.get('country_id') else False,
    #         'state_id': int(post.get('state_id')) if post.get('state_id') else False,
    #         'city': post.get('city'),
    #         'street': post.get('street'),
    #         'zip': post.get('zip'),
    #         'is_librarian': True,
    #         'resume':pdf_base64,
    #         'resume_filename': resume_base64.filename,
    #     }
    #     if post.get('city_id'):
    #         vals['city_id'] = int(post.get('city_id'))
    #     request.env['res.partner'].create(vals)
    #     return request.redirect('/librarians')