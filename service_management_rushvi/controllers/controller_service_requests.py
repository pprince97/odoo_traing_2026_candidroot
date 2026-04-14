from odoo import models, fields, api, http
from odoo.http import request

class ServiceRequestController(http.Controller):

    # @http.route(['/my/service-requests','/my/service-requests/page/<int:page>'], type='http', auth='user', website=True)
    # def view_my_service_requests(self, page=0, **kwargs):
    #     page = int(page)
    #     user = request.env.user
    #     if user.has_group('service_management_rushvi.group_service_admin'):
    #         service_requests = request.env['service.request'].sudo().search([])
    #     elif user.has_group('service_management_rushvi.group_service_owner'):
    #         service_requests = request.env['service.request'].sudo().search([('company_id','in',request.env.user.partner_id.service_company_ids.ids)])
    #     elif user.has_group('service_management_rushvi.group_service_customer'):
    #         service_requests = request.env['service.request'].sudo().search([('customer_id', '=', request.env.user.partner_id.id)])
    #     else:
    #         service_requests = []
    #     total_requests = len(service_requests)
    #
    #     pager = request.website.pager(
    #         url='/my/service-requests',
    #         total=total_requests,
    #         page=page,
    #         step=12,
    #     )
    #     offset = pager['offset']
    #     service_requests = service_requests[offset: offset + 12]
    #     return request.render('service_management_rushvi.service_requests_template', {
    #         'service_requests': service_requests,
    #         'user': request.env.user,
    #         'service_request_count': len(service_requests),
    #         'page_name': 'service_request',
    #         'pager': pager,
    #     })

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

    # @http.route('/my/service-requests/<int:id>/download', type='http', auth='user', website=True)
    # def download_sale_order(self, id, **kwargs):
    #
    #     service_request = request.env['service.request'].sudo().browse(id)
    #     if not service_request.exists():
    #         return request.not_found()
    #
    #     sale_order = service_request.sale_order_id
    #     if not sale_order:
    #         return request.not_found()
    #
    #     report = request.env['ir.actions.report']._get_report_from_name(
    #         'sale.report_saleorder'
    #     ).sudo()
    #     pdf, _ = report._render_qweb_pdf(sale_order.id)
    #     return request.make_response(pdf, headers=[
    #         ('Content-Type', 'application/pdf'),
    #         ('Content-Disposition', f'attachment; filename="{sale_order.name}.pdf"')
    #     ])