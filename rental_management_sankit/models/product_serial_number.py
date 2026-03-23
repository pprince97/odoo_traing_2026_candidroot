from odoo import api, fields, models


class ProductSerialNumber(models.Model):
    _name = 'product.serial.number'
    _description = 'Product Serial Number'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number')
    ref = fields.Char(string='Reference')
    product_id = fields.Many2one('product.template',string='Product')

    available = fields.Boolean(string='Available',default=True)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for val in vals_list:
    #         val['serial_number'] = self.env['ir.sequence'].next_by_code('product.seq')
    #     res = super().create(vals_list)
    #     return res



