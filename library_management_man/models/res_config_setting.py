from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # fine_amount =fields.Boolean(config_parameter="fine_amount")
    fine_amount_value= fields.Float("Fine Amount", config_parameter="library_management_man.fine_amount_value" )
