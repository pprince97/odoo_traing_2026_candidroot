from odoo import api, fields, models, Command

class Company(models.Model):
    _name = 'service.company'
    _description = 'Service Company Model'

    name = fields.Char(string='Company Name',required=True)
    description = fields.Text(string='Description')
    address = fields.Char(string='Address')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    website = fields.Char('Website Link')
    owner_id = fields.Many2one('res.users', string='Owner',required=True)
    # category_ids = fields.Many2many('service.category','company_category_rel','company_id','category_id',string='Service categories')


class CompanyUser(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            if self.env.context.get('customer'):
                rec.group_ids = [Command.set([self.env.ref('service_management_urvi.group_service_customer').id])]
            if self.env.context.get('owner'):
                rec.group_ids = [Command.set([self.env.ref('service_management_urvi.group_service_owner').id])]
        return res