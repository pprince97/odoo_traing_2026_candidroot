from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError

class PartsLines(models.Model):
    _name = "parts.lines"
    _description = "Parts Line"
    _rec_name = 'part_id'

    part_id = fields.Many2one('product.product',string="Parts")
    price = fields.Float(string="Price",related="part_id.list_price")
    maintenance_part_id = fields.Many2one('vehicle.maintenance',string="Maintenance Part ID")