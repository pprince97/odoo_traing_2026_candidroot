from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rental_counts = fields.Integer("Rental Counts", compute="_compute_rental_counts")
    product_counts = fields.Integer("Product Counts", compute="_compute_product_counts")
    rental_object_ids = fields.One2many(
        'rental.object', 'customer_id'
    )

    @api.depends('rental_object_ids')
    def _compute_rental_counts(self):
        counts = self.env['rental.object'].search_count([('customer_id', 'in', self.rental_object_ids.customer_id.id)])
        self.rental_counts = counts

    @api.depends('rental_object_ids.rental_order_lines_ids')
    def _compute_product_counts(self):
        counts = self.env['rental.object.lines'].search_count([('rental_object_id.customer_id', 'in', self.rental_object_ids.customer_id.id)])
        self.product_counts = counts

    def action_open_rental_records(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Records",
            "res_model": "rental.object",
            "view_mode": "list",
            "target": "new",
            "domain": [
                ('customer_id', '=', self.id),
            ],
        }

    def action_open_product_records(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Product Records",
            "res_model": "rental.object.lines",
            "view_mode": "list",
            "target": "new",
            "domain": [
                ('rental_object_id.customer_id', '=', self.id),
            ],
        }