from odoo import api, fields, models

class RentalMaintenance(models.Model):
    _name = 'rental.maintenance'
    _description = 'Rental Maintenance'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one(comodel_name='product.product', string="Vehicle")
    current_km = fields.Integer(string='Current KM')
    arrival_date = fields.Date(string='Arrival Date')
    dispatch_date = fields.Date(string='Dispatch Date')
    part_line_ids = fields.One2many(comodel_name='part.line',inverse_name='maintenance_id')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Foreign Currency")
    total_cost = fields.Monetary(store=True,currency_field='currency_id',string='Total Cost',compute='_compute_total_cost')

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        for rec in self:
            rec.vehicle_id.status = 'maintenance'

    @api.depends('part_line_ids')
    def _compute_total_cost(self):
        for rec in self:
            total = 0
            for part in rec.part_line_ids:
                total += part.sub_cost
            rec.total_cost = total

    def generate_maintenance_bill(self):
        l = []
        res_user = self.env['res.users'].context_get()
        res_partner = self.env['res.users'].browse(res_user['uid']).partner_id
        if self.part_ids:
            for part in self.part_ids:
                l.append((0, 0, {
                    'name': part.name,
                    'price_unit': part.standard_price,
                }))
            create_invoice = self.env['account.move'].with_context(default_move_type='in_invoice').create({
                'partner_id': res_partner.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': l,
                'amount_residual': self.total_cost,
            })
            self.vehicle_id.status = 'maintenance'
            return {
                'type': 'ir.actions.act_window',
                'target': 'self',
                'res_model': 'account.move',
                'res_id': create_invoice.id,
                'view_mode': 'form',
            }
        return True
