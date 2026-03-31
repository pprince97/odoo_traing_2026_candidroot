from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class Services(models.Model):
    _inherit = 'res.partner'

    service_company_ids = fields.One2many('service.company','owner_id',string='Service Company')