from odoo import models,fields,api

class Product(models.Model):
    _inherit = "product.product"

    rental_order_id = fields.Many2one('rental.order',string="Rental Order")


    # def compute_tracking(self):
    #     self.is_storable = True
    #     self.tracking = 'serial'