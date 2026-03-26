from odoo import api, fields, models

class UvPrinting(models.Model):
    _name = 'product.uv.printing'
    _description = 'UV Printing'

    name = fields.Char(string="Name")
    start_range = fields.Char(string="Start Range")
    end_range = fields.Char(string="End Range")
    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    cost = fields.Monetary('Cost', currency_field='company_currency_id')

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id