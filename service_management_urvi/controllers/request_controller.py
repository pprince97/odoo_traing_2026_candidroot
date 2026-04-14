from odoo import http, _,fields
from odoo.http import request,content_disposition

class RequestController(http.Controller):

    @http.route(['/my/request','/my/request/page/<int:page>'], type='http', auth='user', website=True)
    def list_request_records(self,page=0,sortby=None, filterby=None,**post):
        request_records = []
        domain=[]
        if request.env.user.has_group('service_management_urvi.group_service_admin'):
            request_records = request.env['service.request'].search([])
        elif request.env.user.has_group('service_management_urvi.group_service_owner'):
            request_records = request.env['service.request'].search([('category_id.company_id.owner_id','in',request.env.user.id)])
            domain += [('category_id.company_id.owner_id','in',request.env.user.id)]
        else:
            request_records = request.env['service.request'].search(
                [('customer_id', 'in', request.env.user.id)])
            domain += [('customer_id','in',request.env.user.id)]

        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'create_date desc'},
            'date_old': {'label': 'Oldest', 'order': 'create_date asc'},
            'name': {'label': 'Name', 'order': 'name'},
        }

        # Default Sort
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings.get(sortby, searchbar_sortings['date'])['order']

        # Filter Options
        searchbar_filters = {
            'all': {'label': 'All', 'domain': []},
            'today': {'label': 'Today', 'domain': [('create_date', '>=', fields.Date.today())]},
        }

        # Default Filter
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters['all'])['domain']

        request_records = request.env['service.request'].search(domain, order=order)

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

    @http.route('/report/download/<int:record_id>', type='http', auth="user")
    def download_report(self, record_id, **kwargs):
        # Retrieve the report action by its XML ID
        report_action = request.env.ref('sale.action_report_saleorder')

        # Generate the PDF content
        pdf_content, _ = report_action._render_qweb_pdf('sale.action_report_saleorder', [record_id])

        # Set response headers for PDF download
        pdf_http_headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', 'attachment; filename="report.pdf";')
        ]
        return request.make_response(pdf_content, headers=pdf_http_headers)

    # @http.route('/report/download/<int:record_id>', type='http', auth="user", website=True)
    # def download_report(self, record_id, **kwargs):
    #     # 1. Generate the PDF content from the report action
    #     report_xml_id = 'sale.action_report_saleorder'
    #     pdf_content, _ = request.env.ref(report_xml_id).sudo()._render_qweb_pdf([record_id])
    #
    #     # 2. Use content_disposition to force an immediate download
    #     # This keeps the user on the current page while downloading
    #     filename = f"Report_{record_id}.pdf"
    #     headers = [
    #         ('Content-Type', 'application/pdf'),
    #         ('Content-Length', len(pdf_content)),
    #         ('Content-Disposition', content_disposition(filename))
    #     ]
    #     return request.make_response(pdf_content, headers=headers)
