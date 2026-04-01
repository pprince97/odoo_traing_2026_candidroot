from odoo import http, _
from odoo.http import request

class RequestController(http.Controller):

    @http.route(['/my/request','/my/request/page/<int:page>'], type='http', auth='user', website=True)
    def list_request_records(self,page=0,**post):
        request_records = []
        if request.env.user.has_group('service_management_urvi.group_service_admin'):
            request_records = request.env['service.request'].search([])
        elif request.env.user.has_group('service_management_urvi.group_service_owner'):
            request_records = request.env['service.request'].search([('category_id.company_id.owner_id','in',request.env.user.id)])
        else:
            request_records = request.env['service.request'].search(
                [('customer_id', 'in', request.env.user.id)])
        pager = request.website.pager(
            url='/my/request',
            total=len(request_records),
            page=page,
            step=6,
        )
        offset = pager['offset']
        request_records = request_records[offset:offset+6]
        return request.render('service_management_urvi.template_view_request', {'requests': request_records,'pager': pager})

    @http.route(['/create/request'], type='http', auth='user', website=True)
    def create_request_record(self,**post):
        return request.render('service_management_urvi.create_request_record')
