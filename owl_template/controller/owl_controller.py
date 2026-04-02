from odoo import http, models, fields, tools, _
from odoo.http import request

class OwlController(http.Controller):

    @http.route('/owl/save_data', type='jsonrpc', auth='public')
    def save_owl_data(self, **kwargs):
        request.env['owl.data.storage'].sudo().create(kwargs)
        return {'status': 'success', 'message': 'Owl data saved'}


