from odoo import api, fields, models


class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request Model'
    _rec_name = 'service_id'

    req_number = fields.Char('Request Number',readonly=True,default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'),('cancel', 'Cancel')],
                             string='Service State', default='draft')
    date = fields.Datetime('Service Date',required=True)
    customer_id = fields.Many2one('res.users', string='Customer',required=True)
    category_id = fields.Many2one('service.category', string='Category',required=True)
    service_id = fields.Many2one('product.template', string='Service',required=True)
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State')
    city_id = fields.Many2one('res.city', string='City')
    street = fields.Char('Street Address')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    price = fields.Float('Price',related='service_id.list_price')

    @api.model
    def default_get(self, fields):
        defaults = super(ServiceRequest, self).default_get(fields)
        if defaults.get('req_number', 'New') == 'New':
            defaults['req_number'] = self.env['ir.sequence'].next_by_code('request.sequence') or 'New'
        return defaults

    def cancel_state(self):
        self.state = 'cancel'

    def confirm_state(self):
        l=[(0, 0, {'product_template_id': self.service_id, 'product_uom_qty': 1, 'price_unit': self.service_id.list_price,'tax_ids':self.service_id.taxes_id.ids,'name': self.service_id.name})]
        sale_order = self.env['sale.order'].with_context({'default_state' : 'sale'}).create({'partner_id':self.customer_id.partner_id.id,'date_order': self.date,'order_line':l})
        self.sale_order_id = sale_order.id
        self.state = 'confirm'


    def done_state(self):
        self.state = 'done'
