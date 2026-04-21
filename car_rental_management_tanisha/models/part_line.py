from odoo import api, fields, models

class PartLine(models.Model):
    _name = 'part.line'
    _description = 'Part Line'

    maintenance_id = fields.Many2one(comodel_name='rental.maintenance', string='Maintenance')
    currency_id = fields.Many2one(related='maintenance_id.currency_id')
    part_id = fields.Many2one(comodel_name='product.product', string='Name')
    price = fields.Float(related='part_id.standard_price')
    quantity = fields.Integer(string='Quantity')
    sub_cost = fields.Monetary(string='Sub Cost',store=True,currency_field='currency_id',compute='_compute_sub_cost')

    @api.depends('part_id','quantity')
    def _compute_sub_cost(self):
        for part in self:
            part.sub_cost = part.price * part.quantity