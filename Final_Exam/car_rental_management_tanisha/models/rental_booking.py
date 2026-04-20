from odoo import api, fields, models

class RentalBooking(models.Model):
    _name = 'rental.booking'
    _description = 'Rental Booking'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(comodel_name='res.users', string='Name')
    phone = fields.Char(related='customer_id.phone', string='Phone', store=True)
    country_id = fields.Many2one(related='customer_id.partner_id.country_id', string='Country')
    state_id = fields.Many2one(related='customer_id.partner_id.state_id', string='State')
    city = fields.Char(related='customer_id.partner_id.city', string='City')
    street = fields.Char(related='customer_id.partner_id.street', string='Street')
    vehicle_line_ids = fields.One2many(comodel_name='vehicle.line',inverse_name='booking_id')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    trip_details = fields.Text(string="Trip Details")
    state = fields.Selection([('draft', 'Draft'), ('inquiry', 'Inquiry'), ('approved', 'Approved'), ('on_going', 'On-going'),
                              ('completed', 'Completed'),('paid', 'Paid'), ('cancelled', 'Cancelled')], string='Status', default='inquiry')
    damage_description = fields.Text(string="Damage Description")
    currency_id = fields.Many2one(comodel_name='res.currency', string="Foreign Currency")
    damage_charges = fields.Monetary(store=True, readonly=False,currency_field='currency_id',string='Damage Charges')
    total_cost = fields.Monetary(store=True,currency_field='currency_id',string='Total Cost',compute='_compute_total_cost')

    @api.depends('vehicle_line_ids')
    def _compute_total_cost(self):
        for rec in self:
            total = 0
            for vehicle in rec.vehicle_line_ids:
                total += vehicle.sub_cost
            rec.total_cost = total

    def generate_booking_invoice(self):
        l = []
        if self.vehicle_line_ids:
            for vehicle in self.vehicle_line_ids:
                l.append((0, 0, {
                    'name': vehicle.vehicle_id.name,
                    'price_unit': vehicle.per_km_cost,
                    'price_subtotal': vehicle.sub_cost,
                }))
            create_invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create({
                'partner_id': self.customer_id.partner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': l,
                'amount_residual': self.total_cost,
            })
            self.state = 'paid'
            return {
                'type': 'ir.actions.act_window',
                'target': 'self',
                'res_model': 'account.move',
                'res_id': create_invoice.id,
                'view_mode': 'form',
            }
        return True

    def generate_booking_report(self):
        a = self.generate_booking_invoice()
        return self.env.ref('car_rental_management_tanisha.booking_report_template').report_action(a['res_id'], config=False)


