from odoo import http
from odoo.http import request
import base64

class StudentWebsite(http.Controller):

    @http.route('/student/profile', type='http', auth='public', website=True)
    def student_profile_form(self, **kw):
        countries = request.env['res.country'].sudo().search([])
        return request.render('library_management.student_profile_template', {
            'countries': countries,
        })

    @http.route('/get_location_data', type='jsonrpc', auth='public', website=True)
    def get_location_data(self, country_id=None, state_id=None, **kw):
        res = {'states': [], 'cities': []}
        if country_id:
            states = request.env['res.country.state'].sudo().search([
                ('country_id', '=', int(country_id))
            ])
            res['states'] = [{'id': s.id, 'name': s.name} for s in states]
        if state_id:
            if 'res.city' in request.env:
                cities = request.env['res.city'].sudo().search([
                    ('state_id', '=', int(state_id))
                ])
                res['cities'] = [{'id': c.id, 'name': c.name} for c in cities]
        return res

    # @http.route('/save_student_profile', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    # def save_profile(self, **post):
    #     file_data = post.get('file_data')
    #     city_name = post.get('city_text')
    #     if post.get('city_id'):
    #         if 'res.city' in request.env:
    #             city_rec = request.env['res.city'].sudo().browse(int(post.get('city_id')))
    #             city_name = city_rec.name
    #     vals = {
    #         'name': post.get('name'),
    #         'email': post.get('email'),
    #         'phone': post.get('phone'),
    #         'street': post.get('address'),
    #         'zip': post.get('zip'),
    #         'country_id': int(post.get('country_id')) if post.get('country_id') else False,
    #         'state_id': int(post.get('state_id')) if post.get('state_id') else False,
    #         'city': city_name,
    #         'company_type': 'person',
    #         'student_code': request.env['ir.sequence'].sudo().next_by_code('student.sequence') or 'New',
    #     }
    #     new_student = request.env['res.partner'].sudo().create(vals)
    #     if file_data and file_data.filename:
    #         request.env['ir.attachment'].sudo().create({
    #             'name': file_data.filename,
    #             'type': 'binary',
    #             'datas': base64.b64encode(file_data.read()),
    #             'res_model': 'res.partner',
    #             'res_id': new_student.id,
    #             'mimetype': 'application/pdf',
    #         })
    #     return request.redirect('/student/profile')

    @http.route('/save_student_profile', type='jsonrpc', auth='user', website=True)
    def save_profile(self, params):
        print('>>>>>>>>>>>>>>>>>>>>>>>>  params')
        file_data = params.pop('attachment_file', False)
        file_name = params.pop('attachment_name', False)
        params['student_code'] = request.env['ir.sequence'].sudo().next_by_code('student.sequence') or 'New'
        new_student = request.env['res.partner'].create(params)
        if file_data and file_name:
            request.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': file_data,
                'res_model': 'res.partner',
                'res_id': new_student.id,
                'mimetype': 'application/pdf',
            })
        return {
            'success': True,
            'redirect_url': '/student',
        }