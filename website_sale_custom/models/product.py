from odoo import models, fields

class ProductSuitable(models.Model):
    _name = 'product.suitable'
    _description = 'Suitable For'

    name = fields.Char(required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    suitable_ids = fields.Many2many('product.suitable', string="Suitable For")