from odoo import fields,models,api

class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'
    _rec_name = 'serial_no'

    serial_no = fields.Char(string='Serial No')
    company_id = fields.Many2one(comodel_name='service.company', string='Company')
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('cancel','Cancel')],default='draft',string='State')
    date = fields.Date(string='Date')
    country_id = fields.Many2one(comodel_name='res.country', string='Country')
    state_id = fields.Many2one(comodel_name='res.country.state', string='State')
    city_id = fields.Many2one(comodel_name='res.city', string='City')
    street_address  = fields.Char(string='Street Address')
    customer_id = fields.Many2one(comodel_name='res.users', string='Customer')
    service_id = fields.Many2one(comodel_name='product.template', string='Service')
    category_id = fields.Many2one(comodel_name='service.category', string='Category')

    @api.model_create_multi
    def create(self, vals_list):
        vals_list[0]['serial_no'] = self.env['ir.sequence'].next_by_code('service.request.seq') or 'New'
        res = super(ServiceRequest, self).create(vals_list)
        return res


