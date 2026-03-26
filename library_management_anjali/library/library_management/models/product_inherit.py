from odoo import models,fields,api,_

class ProductInherit(models.Model):
    _inherit = "product.template"

    product_ids = fields.Many2many('my.product',string="My Product")