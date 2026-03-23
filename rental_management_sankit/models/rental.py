from odoo import api, fields, models


class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'
    _rec_name = 'customer_id'
    rental_number = fields.Char(string='Rental Number')
    customer_id = fields.Many2one('res.partner',string='Customer')
    rent_start_date = fields.Date(string='Start Date')
    rent_end_date = fields.Date(string='End Date')
    total_amount = fields.Integer(string='Total Amount' , compute='_compute_total_amount' , inverse='_inverse_total_amount')

    # product_ids = fields.One2many('product.template','order_id',string='Products')
    # product_ids = fields.Many2many('product.template',string='Product')

    order_ids = fields.One2many('product.order', 'rental_id', string='Order')

    tag_ids = fields.Many2many('res.partner.category',string="Tags")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('rent', 'Rent'),
            ('returned', 'Returned'),
            ('partially_invoiced', 'Partially Invoiced'),
            ('invoiced', 'Invoiced'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        string="State",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['rental_number'] = self.env['ir.sequence'].next_by_code('rental.seq')
        res = super().create(vals_list)
        return res

    def rent_state(self):
        self.update({'state':'rent'})
    def returned_state(self):
        self.update({'state': 'returned'})
    def invoiced_state(self):
        print("------ ,  , -----")
        self.update({'state': 'invoiced'})
    def partially_invoiced_state(self):
        self.update({'state': 'partially_invoiced'})
    def cancelled_state(self):
        self.update({'state': 'cancelled'})
    def draft_state(self):
        self.update({'state': 'draft'})

    @api.depends('order_ids')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = 0
            for order in rec.order_ids:
                count = 0
                for c in order.serial_number_ids:
                    count += 1
                rec.total_amount += order.list_price * count
    def _inverse_total_amount(self):
        for rec in self:
            rec.total_amount = rec.total_amount



