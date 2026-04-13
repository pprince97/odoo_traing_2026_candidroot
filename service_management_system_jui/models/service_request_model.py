from email.policy import default

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'
    _rec_name = 'request_number'

    request_number = fields.Char(string='Request Number',readonly=True)
    date = fields.Date(string='Date')
    category_id = fields.Many2one('service.category',string='Service Categories')
    company_id_s = fields.Many2one('custom.service.company',related="category_id.company_id_s",string='Company')
    service_id = fields.Many2one('product.template',string='Services')
    customer_id = fields.Many2one('res.users',string='Customer')
    country_id = fields.Many2one('res.country','Country')
    state_id = fields.Many2one('res.country.state','State')
    city_id = fields.Many2one('res.city','City Id')
    city = fields.Char(string='City')
    street = fields.Char(string='Street Address')
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('cancel','Cancel')],string='States',default='draft')

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['request_number'] = self.env['ir.sequence'].next_by_code('service.request.seq') or 'New'
        res = super(ServiceRequest, self).create(vals)
        return res

    def confirm_state(self):
        self.state = 'confirm'
        for rec in self:
            order = self.env['sale.order'].with_context({'search_default_sales' : 1}).create({'partner_id': rec.customer_id.partner_id.id,'state':'sale'})
            self.env['sale.order.line'].create({'product_id':rec.service_id.id,'price_unit':rec.service_id.list_price,'order_id':order.id})

    def cancel_state(self):
        self.state = 'cancel'
