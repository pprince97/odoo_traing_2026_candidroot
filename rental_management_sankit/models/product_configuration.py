from odoo import api, fields, models

class ProductConfiguration(models.Model):
    _inherit = 'product.template'

    # name , type  , is_storable , tracking

    serial_number_ids = fields.One2many('product.serial.number','product_id',string='Serial Numbers')
