from odoo import models, fields

class Contact(models.Model):
    _inherit = "res.partner"

    city_id = fields.Many2one('res.city',string='City')
    file_pdf = fields.Binary(string='File PDF')
    file_pdf_name = fields.Char(string='File PDF Name')