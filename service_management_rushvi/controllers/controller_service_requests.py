from odoo import models, fields, api, http
from odoo.http import request
from odoo.exceptions import ValidationError

class ServiceRequestController(http.Controller):

    @http.route(['/my/service-requests','/my/service-requests/page/<int:page>'], type='http', auth='user', website=True)
    def view_my_service_requests(self, page=0, **kwargs):
        page = int(page)
        service_requests = request.env['service.request'].sudo().search([])
        total_requests = len(service_requests)

        pager = request.website.pager(
            url='/my/service-requests',
            total=total_requests,
            page=page,
            step=12,
        )
        offset = pager['offset']
        service_requests = service_requests[offset: offset + 12]
        return request.render('service_management_rushvi.service_requests_template', {
            'service_requests': service_requests,
            'user': request.env.user,
            'service_request_count': len(service_requests),
            'page_name': 'service_request',
            'pager': pager,
        })

    @http.route(['/my/service-requests/<int:id>'], type='http', auth='user', website=True)
    def view_service_request_form(self, id, **post):
        service_request = request.env['service.request'].sudo().browse(id)
        return request.render('service_management_rushvi.service_requests_template_form', {
            'service_request': service_request,
            'page_name': 'service_request',
            'service_requests_lines': service_request,
            'user': request.env.user,
        })

    @http.route(['/my/service-requests/new'], type='http', auth='public', website=True)
    def view_service_request_form(self):
        return request.render('service_management_rushvi.portal_service_create_form',{})