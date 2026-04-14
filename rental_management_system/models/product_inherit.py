from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products:
            product.is_storable = True
            product.tracking = 'serial'
        return products
