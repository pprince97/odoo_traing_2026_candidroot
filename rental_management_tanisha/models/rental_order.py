from odoo import models,fields,api,_

from odoo.exceptions import ValidationError


class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'
    _rec_name = 'serial_no'

    serial_no = fields.Char(string='Serial No')
    customer_id = fields.Many2one('res.partner',string='Customer')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    product_ids = fields.Many2many(comodel_name='product.product', relation='product_rent_rel', column1='rental_order_id', column2='product_id', string='Products')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    total_amount = fields.Monetary(store=True, readonly=False, currency_field='currency_id', string='Total Amount', compute='_compute_total_amount')
    state = fields.Selection(selection=[('draft','Draft'),('rent','Rent'),('returned','Returned'),('invoiced','Invoiced'),('partially_invoiced','Partially Invoiced'),('cancelled','Cancelled')],string='State', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        vals_list[0]['serial_no'] = self.env['ir.sequence'].next_by_code('rental.order.seq') or 'New'
        res = super(RentalOrder, self).create(vals_list)
        return res

    @api.depends('start_date','end_date','product_ids')
    def _compute_total_amount(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.start_date < rec.end_date:
                    total = 0
                    days = (rec.end_date - rec.start_date).days
                    for product in rec.product_ids:
                        total += product.lst_price
                    rec.total_amount = total * days
                else:
                    raise ValidationError('Start date must be less than end date')