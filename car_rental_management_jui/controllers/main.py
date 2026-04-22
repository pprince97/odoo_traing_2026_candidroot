from odoo import http, _,fields, Command
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.fields import Domain


class CarRentalManagementController(http.Controller):

    @http.route(['/my/car/rental/bookings','/my/car/rental/bookings/page/<int:page>'], type='http', auth='user', website=True)
    def car_rental_bookings_controller(self,page=0, **kwargs):
        domain = []
        total = request.env['vehicle.booking'].search_count(domain)
        pager = request.website.pager(
            url='/my/car/rental/bookings',
            total=total,
            page=page,
            step=3,
        )
        offset = pager['offset']
        values = request.env['vehicle.booking'].search(domain)
        values = values[offset: offset + 3]

        return request.render('car_rental_management_jui.car_rental_bookings_template_list',{'requests': values,'pager': pager,
            'default_url': '/my/car/rental/bookings'})

    @http.route(['/my/car/rental/bookings/view/<int:res_id>'], type='http', auth='user',website=True)
    def car_rental_bookings_view_controller(self, res_id, **kwargs):
        record = request.env['vehicle.booking'].browse(res_id)
        return request.render('car_rental_management_jui.car_rental_bookings_template_view', {
            'record': record,
        })

    @http.route(['/my/rental/print/<int:res_id>'], type='http', auth="user", website=True)
    def print_rental_invoice(self, res_id, **kw):
        invoice = request.env['vehicle.booking'].browse(res_id)
        if not invoice.exists():
            return request.not_found()
        pdf, _ = request.env['ir.actions.report']._render_qweb_pdf('car_rental_management_jui.report_booking', [res_id])

        pdf_http_headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename="Invoice_%s.pdf"' % invoice.invoice_id.name)
        ]
        return request.make_response(pdf, headers=pdf_http_headers)

    @http.route('/my/car/rental/bookings/form/', type='http', auth='public', website=True)
    def car_rental_bookings_form_controller(self, **kwargs):
        request_id = request.session.get('booking_id')

        _booking = None
        if request_id:
            _booking = request.env['vehicle.booking'].browse(request_id)

        values = {
            'requests': _booking or {},
            'id': _booking.id if _booking else False,
        }
        return request.render('car_rental_management_jui.car_rental_bookings_template_form', values)

    @http.route('/my/car/rental/bookings/form/submit', type='http', auth='user', website=True, methods=['POST'])
    def car_rental_bookings_form_submit_controller(self, **post):

        Booking = request.env['vehicle.booking']
        BookingLine = request.env['vehicle.booking.line']

        request_id = request.session.get('booking_id')

        if not request_id:
            _booking = Booking.create({
                'customer_id': int(post.get('customer_id')) if post.get('customer_id') else False,
                'state': post.get('state') or 'draft',
                'rent_date': post.get('rent_date'),
                'return_date': post.get('return_date'),
                'trip_place': post.get('trip_place'),
            })
            request.session['booking_id'] = _booking.id
        else:
            _booking = Booking.browse(request_id)

        if post.get('action') == 'add_line':
            if post.get('new_vehicle_id') and post.get('new_driver_id'):
                BookingLine.create({
                    'booking_id': _booking.id,
                    'vehicle_id': int(post.get('new_vehicle_id')) if post.get('new_vehicle_id') else False,
                    'driver_id': int(post.get('new_driver_id')) if post.get('new_driver_id') else False,
                    'start_km': int(post.get('new_start_km') or 1),
                    'end_km': int(post.get('new_end_km') or 1),
                })

            return request.redirect('/my/car/rental/bookings/form/')

        request.session.pop('booking_id', None)

        return request.render('car_rental_management_jui.thank_you')

    @http.route('/car/rental/booking/line/delete/<int:line_id>', type='http', auth='public', website=True)
    def delete_line(self, line_id, **kw):
        line = request.env['vehicle.booking.line'].browse(line_id)
        if line:
            line.unlink()
        return request.redirect('/my/car/rental/bookings/form/')

    @http.route('/availability/domain/filter', type='jsonrpc', auth='user', website=True)
    def availability_filter(self, rent_date_s,return_date_s):
        if rent_date_s and return_date_s:
            rent_date = fields.Date.to_date(rent_date_s)
            return_date = fields.Date.to_date(return_date_s)
            domain = Domain.OR([Domain([('rent_date', '<=', rent_date),
                                        ('return_date', '>=', rent_date)]),
                                Domain([('rent_date', '<=', return_date),
                                        ('return_date', '>=', return_date)]),
                                Domain([('rent_date', '>=', rent_date),
                                        ('return_date', '<=', return_date)])])
            domain &= Domain(
                [('state', 'in', ['draft', 'approved', 'inquiry', 'on_going'])])
            id_s1 = self.env['vehicle.booking'].search(domain).booking_line_ids.vehicle_id.ids
            id_s2 = self.env['product.product'].search([('is_vehicle', '=', True)]).ids
            data_v = list(set(id_s2) - set(id_s1))
            available_vehicles = self.env['product.product'].search_read(
                [('id', 'in', data_v)],
                ['id', 'display_name']
            )

            id_s3 = self.env['vehicle.booking'].search(domain).booking_line_ids.driver_id.ids
            id_s4 = self.env['res.partner'].search([('is_driver', '=', True)]).ids
            data_d = list(set(id_s4) - set(id_s3))
            available_drivers = self.env['res.partner'].search_read(
                [('id', 'in', data_d)],
                ['id', 'display_name']
            )
        return {'available_vehicles': available_vehicles, 'available_drivers':available_drivers}
