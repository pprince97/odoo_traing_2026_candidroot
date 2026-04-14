from odoo import models, fields, api
# from datetime import date
# from odoo.exceptions import ValidationError


class RentalObject(models.Model):
    _name = 'rental.object'
    _description = 'Rental Object'

    serial_number = fields.Char(string='Serial Number', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    return_date = fields.Date(string='Returned Date')
    start_date = fields.Date(string='Start Date')
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("rent", "Rent"),
            ("returned", "Returned"),
            ("invoiced", "Invoiced"),
            ("partially_invoiced", "Partially Invoiced"),
            ("cancelled", "Cancelled")
        ],
        string="State",
        default="draft"
    )
    rental_order_lines_ids = fields.One2many(
        'rental.object.lines', 'rental_object_id', string='Rental Order Lines'
    )
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')

    @api.depends('rental_order_lines_ids')
    def _compute_total_amount(self):
        for lot in self:
            lot.total_amount = sum(lot.rental_order_lines_ids.mapped('total_amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('rental.sequence') or 'New'
        return super().create(vals_list)

    def action_rent(self):
        for rec in self:
            rec.rental_order_lines_ids.lot_ids.is_available = False
            rec.update({"state": "draft"})

    def action_return(self):
        for rec in self:
            rec.rental_order_lines_ids.lot_ids.is_available = True
            rec.update({"state": "draft"})

    def action_invoice(self):
        self.update({"state": "invoiced"})

    def action_cancel(self):
        self.update({"state": "cancelled"})