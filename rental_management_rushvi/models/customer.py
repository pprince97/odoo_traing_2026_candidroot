from odoo import models,fields,api

class Customer(models.Model):
    _inherit = "res.partner"

    rental_order_count = fields.Integer(string="Number of Rental Orders",compute="_compute_rental_order_count")
    rental_product_count = fields.Integer(string="Number of Rental Products",compute="_compute_rental_product_count")
    rental_order_ids = fields.One2many('rental.order','customer_id',string="Rental Orders")

    def _compute_rental_order_count(self):
        for rec in self:
            rec.rental_order_count = len(rec.rental_order_ids)

    def _compute_rental_product_count(self):
        count = 0
        for rec in self.rental_order_ids:
            count += len(rec.rental_order_line_ids)
        self.rental_product_count = count

    def view_rental_orders(self):
        return {
            'name': 'Rental Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'rental.order',
            'view_mode': 'list,form',
            'domain': [('customer_id', '=', self.id)],
            'target': 'current',
            'context': {'default_customer_id': self.id},
        }

    def view_rental_products(self):
        return {
            'name': 'Rental Products',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('rental_order_id', 'in', self.rental_order_ids.ids)],
            'target': 'current',
        }