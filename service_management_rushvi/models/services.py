from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class Services(models.Model):
    _inherit = 'product.template'

    service_category_id = fields.Many2one('service.category',string='Service Category')
    service_company_id = fields.Many2one('service.company',string='Service Company')

    @api.onchange('service_category_id')
    def _onchange_category_id(self):
        if self.service_category_id:
            self.service_company_id = self.service_category_id.company_id
        else:
            self.service_company_id = False