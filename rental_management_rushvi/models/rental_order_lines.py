from odoo import models,fields,api

class RentalOrderLines(models.Model):
    _name = "rental.order.lines"
    _description = "Rental Order Lines"

    rental_order_id = fields.Many2one('rental.order',string="Rental Orders")
    currency_id = fields.Many2one('res.currency',string="Currency")
    total_amount = fields.Float(string="Total Amount(per day)",compute="_compute_amount")
    product_id = fields.Many2one('product.product',string="Product")
    lot_id = fields.Many2one('stock.lot',string="Lots")
    product_amount = fields.Float(string="Amount",compute="_compute_amount")

    @api.depends('product_id','lot_id')
    def _compute_amount(self):
        for rec in self:
            rec.product_amount = rec.product_id.lst_price
            rec.total_amount = rec.product_amount * len(rec.lot_id)