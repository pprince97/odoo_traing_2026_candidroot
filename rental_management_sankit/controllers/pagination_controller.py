from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class FleetPortal(CustomerPortal):
    @http.route([
        '/fleet',
        '/fleet/page/<int:page>',
    ], type='http', auth='user', website=True)
    def portal_fleet(
        self,
        page=1,
        search=None,
        search_in='all',
        filterby='all',
        date_begin=None,
        date_end=None,
        sortby=None,
        **kwargs
    ):
        Fleet = request.env['fleet.vehicle'].sudo()
        print(Fleet,"-----------0------:")
        searchbar_inputs = {
            'all': {
                'label': 'All',
                'input': 'all',
                'domain': [],
            },
            'name': {
                'label': 'Vehicle Name',
                'input': 'name',
                'domain': [('name', 'ilike', search)] if search else [],
            },
            'license_plate': {
                'label': 'License Plate',
                'input': 'license_plate',
                'domain': [('license_plate', 'ilike', search)] if search else [],
            },
            'status': {
                'label': 'Status',
                'input': 'status',
                'domain': [('state_id.name', 'ilike', search)] if search else [],
            },
        }
        searchbar_filters = {
            'all': {
                'label': 'All',
                'domain': [],
            },
            'registered': {
                'label': 'Registered',
                'domain': [('state_id.name', '=', 'Registered')],
            },
            'downgraded': {
                'label': 'Downgraded',
                'domain': [('state_id.name', '=', 'Downgraded')],
            },
        }
        search_domain = searchbar_inputs.get(search_in, searchbar_inputs['all'])['domain']
        filter_domain = searchbar_filters.get(filterby, searchbar_filters['all'])['domain']
        base_domain = [('driver_id', '=', request.env.user.partner_id.id)]
        domain =  search_domain + filter_domain
        total_vehicles = Fleet.search_count(domain)
        step = 3
        pager = portal_pager(
            url='/fleet',
            url_args={
                'search': search,
                'search_in': search_in,
                'filterby': filterby,
                'sortby': sortby,
                'date_begin': date_begin,
                'date_end': date_end,
            },
            total=total_vehicles,
            page=page,
            step=step,
        )
        fleet_records = Fleet.search(
            domain,
            limit=step,
            offset=pager['offset'],
            order='name asc',
        )
        values = {
            'fleet_records': fleet_records,
            'page_name': 'fleet',
            'default_url': '/fleet',
            'pager': pager,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'sortby': sortby,
            'date_begin': date_begin,
            'date_end': date_end,
        }
        return request.render('rental_management_sankit.portal_fleet_template', values)
