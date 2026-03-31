from odoo import fields,models,api

class Services(models.Model):
    _inherit = 'product.template'
    _rec_name = 'category_id'

    category_id = fields.Many2one(comodel_name='service.category', string='Category')
    belong_company_id = fields.Many2one(comodel_name='service.company', string='Company')

