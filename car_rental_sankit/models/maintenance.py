from odoo import api, fields, models
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError

class Maintenance(models.Model):
    _name = 'car.maintenance'
    _description = 'Maintenance'
    _rec_name = 'vehicle_id'

    company_id = fields.Many2one('res.company')
    vehicle_id = fields.Many2one('product.product',string="Vehicle")
    current_km = fields.Float(string="Current Km")
    arrival_date = fields.Date(string="Arrival Date")
    dispatch_date = fields.Date(string="Dispatch Date")

    parts_ids = fields.Many2many('product.product',string="Parts")

    status = fields.Selection([
        ('arrival', 'Arrival'),
        ('in_process', 'In Process'),
        ('dispatch', 'Dispatch'),
    ],
        default='arrival',
        string="Status",
    )

    def in_process_status(self):
        self.vehicle_id.update({'status': 'maintenance'})
        self.update({'status': 'in_process'})

    def dispatch_status(self):
        l = []
        for part in self.parts_ids:
            l.append((0, 0, {'name': part.name, 'quantity': 1, 'price_unit': part.standard_price}))
        self.env['account.move'].with_context({'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.company_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l})
        self.vehicle_id.update({'status': 'available'})
        self.update({'status': 'dispatch'})

    def arrival_status(self):
        self.update({'status': 'arrival'})
