from odoo import models, fields, api, http
from odoo.http import request

class ServiceRequestController(http.Controller):

    @http.route(['/my/service-requests/<int:id>'], type='http', auth='user', website=True)
    def view_service_request_form(self, id, **post):
        service_request = request.env['service.request'].sudo().browse(id)
        if service_request.sale_order_id:
            service_request.sale_order_id._portal_ensure_token()
        return request.render('service_management_rushvi.service_requests_template_form', {
            'service_request': service_request,
            'page_name': 'service_request',
            'service_requests_lines': service_request,
            'user': request.env.user,
        })