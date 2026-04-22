from odoo import api, fields, models, _, Command
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class RentalBooking(models.Model):
    _name = 'rental.booking'
    _description = 'Rental Booking'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(comodel_name='res.partner', string='Name')
    phone = fields.Char(related='customer_id.phone', string='Phone', store=True)
    country_id = fields.Many2one(related='customer_id.country_id', string='Country')
    state_id = fields.Many2one(related='customer_id.state_id', string='State')
    city = fields.Char(related='customer_id.city', string='City')
    street = fields.Char(related='customer_id.street', string='Street')
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
    total_days = fields.Integer(compute='_compute_total_days',store=True)
    vehicles = fields.Many2many(comodel_name='product.product',relation='booking_product_rel', column1='booking_id', column2='product_id', compute='_compute_vehicles')
    drivers = fields.Many2many(comodel_name='res.partner',relation='booking_partner_rel', column1='booking_id', column2='partner_id', compute='_compute_vehicles')


    def state_inquiry(self):
        self.state = 'inquiry'

    def state_approved(self):
        self.state = 'approved'

    def state_on_going(self):
        self.state = 'on_going'

    def state_completed(self):
        self.state = 'completed'

    def state_paid(self):
        self.state = 'paid'

    def state_cancelled(self):
        self.state = 'cancelled'

    @api.depends('vehicle_line_ids','start_date', 'end_date')
    def _compute_vehicles(self):
        domain = Domain.OR([
            Domain([('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date)]),
            Domain([('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)]),
            Domain([('start_date', '>=', self.start_date), ('end_date', '<=', self.end_date)])])
        vehicles_1 = self.env['rental.booking'].search(domain)['vehicle_line_ids']['vehicle_id']
        vehicles_2 = self.env['product.product'].search([('type', '=', 'vehicle')])
        vehicles_3 = self.env['rental.booking'].browse(self.ids)['vehicle_line_ids']['vehicle_id']
        self.write({
            'vehicles': [Command.set((vehicles_2 - vehicles_1 - vehicles_3).ids)],
        })
        drivers_1 = self.env['rental.booking'].search(domain)['vehicle_line_ids']['driver_id']
        drivers_2 = self.env['res.partner'].search([('is_driver', '=', True)])
        drivers_3 = self.env['rental.booking'].browse(self.ids)['vehicle_line_ids']['driver_id']
        self.write({
            'drivers': [Command.set((drivers_2 - drivers_1 -drivers_3).ids)],
        })

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(_("Start date must be less than End date!!!!!!"))

    @api.depends('start_date', 'end_date')
    def _compute_total_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.total_days = (rec.end_date - rec.start_date).total_seconds()/(60*60*24)
            else:
                rec.total_days = 0
            self._compute_vehicles()

    @api.depends('vehicle_line_ids','damage_charges','total_days')
    def _compute_total_cost(self):
        for rec in self:
            total = 0
            for vehicle in rec.vehicle_line_ids:
                total += vehicle.sub_cost
            rec.total_cost = total*rec.total_days + rec.damage_charges

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
                'partner_id': self.customer_id.id,
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






