from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'

    name = fields.Char(string='Service Number')
    category_id = fields.Many2one('service.category',string='Category',required=True)
    company_id = fields.Many2one('service.company',string='Company',required=True)
    customer_id = fields.Many2one('res.partner',string='Customer',required=True)
    state_id = fields.Many2one('res.country.state',string='State')
    country_id = fields.Many2one('res.country',string='Country')
    status = fields.Selection([('draft','draft'),('confirmed','confirmed'),('done','Done'),('cancelled','cancelled')],string='Status',default='draft')
    zip = fields.Char(string='Zip')
    city = fields.Char(string='City')
    request_line_ids = fields.One2many('service.request.lines','request_id',string='Requests')
    service_date = fields.Datetime(string='Service Date')
    # sale_order_id = fields.Many2one('sale.order',string='Sale Order')

    def status_confirmed(self):
        products = []
        for product in self.request_line_ids:
            products.append((0, 0, {
                'name': product.service_id.name,
                'product_uom_qty': product.quantity,
                'price_unit': product.amount,
            }))
        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer_id.id,
            'state': 'sale',
            'partner_invoice_id': self.company_id.id,
            'partner_shipping_id': self.customer_id.id,
            'date_order':self.service_date,
            'order_line': products,
        })
        self.status = 'confirmed'

    def status_done(self):
        self.status = 'done'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ServiceRequest, self).create(vals_list)
        for rec in res:
            rec.name = self.env['ir.sequence'].next_by_code('service.request.sequence')
        return res

    def status_cancelled(self):
        self.status = 'cancelled'

    @api.onchange('service_date')
    def onchange_service_date(self):
        if self.service_date and self.service_date <= fields.Datetime.now():
            raise ValidationError("Service Date cannot be in Past")

    @api.onchange('category_id')
    def onchange_category_id(self):
        if self.category_id:
            self.company_id = self.category_id.company_id.id
        else:
            self.company_id = False

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            self.zip = self.customer_id.zip
            self.city = self.customer_id.city
            self.country_id = self.customer_id.country_id.id
            self.state_id = self.customer_id.state_id.id
        else:
            self.zip = False
            self.city = False
            self.country_id = False
            self.state_id = False