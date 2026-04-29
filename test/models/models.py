from odoo import api,fields,models,tools

class Test(models.Model):
    _inherit = 'sale.order'

    def _get_confirmation_template(self):
        pass