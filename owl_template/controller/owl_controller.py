from odoo import http, models, fields, tools, _
from odoo.http import request

class OwlController(http.Controller):

    @http.route('/owl/save_data', type='jsonrpc', auth='public')
    def save_owl_data(self, **kwargs):
        request.env['owl.data.storage'].sudo().create(kwargs)
        return {'status': 'success', 'message': 'Owl data saved!'}

    @http.route('/pos/has_draft_order', type='jsonrpc', auth='user')
    def has_draft_order(self, table_id=None, **kwargs):
        order_count = request.env['pos.order'].search_count([
            ('table_id', '=', table_id),
            ('state', '=', 'draft')
        ])
        return order_count > 0
