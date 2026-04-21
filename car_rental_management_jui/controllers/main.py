from odoo import http, _,fields
from odoo.http import request
from odoo.exceptions import AccessError

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
                request.env['product.product'].browse(int(post.get('new_vehicle_id'))).write({'status':'booked'})
                request.env['res.partner'].browse(int(post.get('new_driver_id'))).write({'status':False})

            return request.redirect('/my/car/rental/bookings/form/')

        request.session.pop('booking_id', None)

        return request.render('car_rental_management_jui.thank_you')

    @http.route('/car/rental/booking/line/delete/<int:line_id>', type='http', auth='public', website=True)
    def delete_line(self, line_id, **kw):
        line = request.env['vehicle.booking.line'].browse(line_id)
        if line:
            line.unlink()
        return request.redirect('/my/car/rental/bookings/form/')