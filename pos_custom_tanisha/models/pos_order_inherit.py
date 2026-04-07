from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_date_time = fields.Datetime()
    end_date_time = fields.Datetime()



