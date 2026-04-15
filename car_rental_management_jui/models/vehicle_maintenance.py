from odoo import api, fields, models

class VehicleMaintenance(models.Model):
    _name = "vehicle.maintenance"
    _description = "Vehicle Maintenance"
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product',string="Vehicle",required=True)
    current_km = fields.Float(string="Current Km",required=True)
    arrival_date = fields.Datetime(string="Arrival Date",readonly=True)
    dispatch_date = fields.Datetime(string="Dispatch Date",readonly=True)
    parts_ids = fields.One2many('parts.lines','maintenance_part_id',string="Parts IDs")
    status = fields.Selection([('on_going','On Going'),('completed','Completed'),('paid','Paid')],string="Status",default='on_going')
    total_cost = fields.Float(string="Total Cost",compute="_compute_total_cost",store=True)

    def status_completed(self):
        self.vehicle_id.status = 'available'
        self.dispatch_date = fields.Date.today()
        self.status = 'completed'

    def status_paid(self):
        res = self.env['account.move'].with_context(
            {'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.env.user.partner_id.id, 'invoice_date': fields.Date.today()})
        for line in self.parts_ids:
            self.env['account.move.line'].create(
                {'move_id': res.id, 'product_id': line.part_id.id, 'price_unit': line.price})
        res.update({'state': 'posted'})
        self.status = 'paid'

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            vehicle = self.env['product.product'].browse(val['vehicle_id'])
            vehicle.status = 'maintenance'
            val['arrival_date'] = fields.Date.today()
        res = super(VehicleMaintenance, self).create(vals)
        return res

    @api.depends('parts_ids')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = 0
            if rec.parts_ids:
                for line in rec.parts_ids:
                    rec.total_cost += line.price