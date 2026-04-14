from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.fields import Domain
from collections import OrderedDict

class ServiceRequestPortal(CustomerPortal):

    @http.route(['/my/my-services/download/<int:order_id>'], type='http', auth="public", website=True)
    def download_sale_order_report(self, order_id, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except Exception:
            return request.redirect('/my/home')
        return self._show_report(
            model=order_sudo,
            report_type='pdf',
            report_ref='sale.action_report_saleorder',
            download=True
        )

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'service_count' in counters:
            values['service_count'] = request.env['service.request'].search_count([])
        return values

    @http.route(['/my/service-requests', '/my/service-requests/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_service_requests(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        if user.has_group('service_management_rushvi.group_service_admin'):
            base_domain = []
        elif user.has_group('service_management_rushvi.group_service_owner'):
            base_domain = [('company_id', 'in', user.partner_id.service_company_ids.ids)]
        elif user.has_group('service_management_rushvi.group_service_customer'):
            base_domain = [('customer_id', '=', user.partner_id.id)]
        else:
            base_domain = [('id', '=', 0)]
        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'service_date desc'},
            'name': {'label': 'Reference', 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        searchbar_filters = {
            'all': {'label': 'All', 'domain': base_domain},
            'draft': {'label': 'Draft', 'domain': base_domain + [('status', '=', 'draft')]},
            'confirmed': {'label': 'Confirmed', 'domain': base_domain + [('status', '=', 'confirmed')]},
            'done': {'label': 'Done', 'domain': base_domain + [('status', '=', 'done')]},
        }
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        # if kw.get('company_id'):
        #     domain += [('company_id', '=', int(kw.get('company_id')))]
        # if kw.get('category_id'):
        #     domain += [('category_id', '=', int(kw.get('category_id')))]
        # if date_begin and date_end:
        #     domain += [('service_date', '>', date_begin), ('service_date', '<=', date_end)]
        ServiceRequest = request.env['service.request'].sudo()
        service_count = ServiceRequest.search_count(domain)
        pager = request.website.pager(
            url='/my/service-requests',
            url_args={'sortby': sortby, 'filterby': filterby},
            total=service_count,
            page=page,
            step=12,
        )
        # 'date_begin': date_begin, 'date_end': date_end,
        requests = ServiceRequest.search(domain, order=order, limit=12, offset=pager['offset'])
        values.update({
            'service_requests': requests,
            'page_name': 'service_request',
            'pager': pager,
            'default_url': '/my/service-requests',
            'searchbar_sortings': searchbar_sortings,
            'service_request_count': service_count,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("service_management_rushvi.service_requests_template", values)

