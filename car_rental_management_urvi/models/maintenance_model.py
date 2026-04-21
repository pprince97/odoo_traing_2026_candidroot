from odoo import fields, models


class Maintenance(models.Model):
    _name = 'car.rental.maintenance'
    _description = 'Maintenance'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product', string='Vehicle')
    current_km = fields.Integer(string='Current KM')
    arrival_date = fields.Date(string='Arrival Date', default=fields.Date.today(), readonly=True)
    dispatch_date = fields.Date(string='Dispatch Date', readonly=True)
    maintenance_lines = fields.One2many('car.rental.maintenance.lines', 'maintenance_id', string='Maintenance Lines')
    state = fields.Selection(
        [('pending', 'Pending'), ('in_process', 'In Process'), ('completed', 'Completed'), ('paid', 'Paid')],
        string='State', default='pending')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    bill_id = fields.Many2one('account.move', string='Bill')

    def in_process_state(self):
        self.state = 'in_process'

    def completed_state(self):
        self.state = 'completed'
        self.dispatch_date = fields.Date.today()
        self.vehicle_id.status = 'maintenance'

    def generate_bill(self):
        bill_lines = []
        for line in self.maintenance_lines:
            bill_lines.append((0, 0, {
                'name': line.part_id.name or ("Maintenance Service"),
                'quantity': 1,
                'price_unit': line.cost,
            }))

        bill = self.env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': self.env.company.partner_id.id,
                'invoice_date': fields.Date.today(),
                'date': fields.Date.today(),
                'invoice_line_ids': bill_lines,
                'ref': f"Maint: {self.vehicle_id.name} ({self.arrival_date})",
            })

        self.bill_id = bill.id
        self.state = 'paid'

        return {
            'name': ('Maintenance Bill'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': bill.id,
            'type': 'ir.actions.act_window',
        }

    def _compute_total_cost(self):
        self.total_cost = 0
        for rec in self.maintenance_lines:
            self.total_cost += rec.cost


class MaintenanceLines(models.Model):
    _name = 'car.rental.maintenance.lines'
    _description = 'Maintenance Lines'
    _rec_name = 'maintenance_id'

    part_id = fields.Many2one('product.product', string='Part ID')
    cost = fields.Float(string='Cost', related='part_id.lst_price')
    maintenance_id = fields.Many2one('car.rental.maintenance', string='Maintenance')
