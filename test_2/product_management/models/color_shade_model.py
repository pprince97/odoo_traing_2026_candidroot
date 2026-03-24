from odoo import api, fields, models

class ColorShade(models.Model):
    _name = 'product.color.shade'
    _description = 'Color Shade'

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    cost = fields.Monetary('Cost', currency_field='company_currency_id')

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id