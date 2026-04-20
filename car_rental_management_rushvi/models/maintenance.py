from odoo import api, fields, models, tools

class Maintenance(models.Model):
    _name = 'car.rent.maintenance'
    _description = 'Maintenance'
    _rec_name = 'vehicle_id'

    status = fields.Selection([('draft','Draft'),('arrived','Arrived'),('paid','Paid'),('dispatched','Dispatched'),('canceled','canceled')],string='Status',default='draft')
    vehicle_id = fields.Many2one('product.product',string='Vehicle', domain=[('vehicle_code','!=',False)])
    current_kms = fields.Float(string='Current Kms')
    arrival_date = fields.Date(string='Arrival Date')
    dispatch_date = fields.Date(string='Dispatch Date')
    parts_added_ids = fields.One2many('product.product','maintenance_id',string='Parts Add')
    service_cost = fields.Float(string='Service Cost')
    parts_cost = fields.Float(string='Parts Cost',default=0,store=True)
    total_cost = fields.Float(string='Total Cost',compute='_compute_total_cost',store=True)
    bill_id = fields.Many2one('account.move',string='Bill')

    def status_arrived(self):
        self.env['product.product'].search([('id','=',self.vehicle_id.id)],limit=1).status = 'maintenance'
        self.status = 'arrived'

    def status_dispatched(self):
        self.env['product.product'].search([('id','=',self.vehicle_id.id)],limit=1).status = 'available'
        self.status = 'dispatched'

    def status_canceled(self):
        self.status = 'canceled'

    def status_paid(self):
        invoice_lines = []
        for task in self.parts_added_ids:
            invoice_lines.append((0, 0, {
                'name': task.name,
                'quantity': 1.0,
                'price_unit': task.lst_price,
            }))
        invoice_lines.append((0, 0, {
            'name': "Service Cost",
            'quantity': 1.0,
            'price_unit': self.service_cost,
        }))
        move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.env.user.company_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        })
        move.write({
            'state': 'posted',
        })
        self.bill_id = move
        self.status = 'paid'

    @api.onchange('parts_added_ids')
    def onchange_parts_added_ids(self):
        self.parts_cost = sum(self.parts_added_ids.mapped('lst_price'))

    @api.depends('parts_added_ids', 'service_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.service_cost + rec.parts_cost