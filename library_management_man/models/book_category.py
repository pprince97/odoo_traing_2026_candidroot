from odoo import models, fields, api

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book category'

    name = fields.Char(string="Name", required=True)
