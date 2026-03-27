from odoo import api, fields, models, exceptions

class Customer(models.Model):
    _inherit = 'res.partner'

    document = fields.Binary(string="Upload Document", attachment=True)
    doc_name = fields.Char(string="Document Name")