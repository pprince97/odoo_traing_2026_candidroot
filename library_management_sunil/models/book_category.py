from odoo import models, fields


class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book Category'

    name = fields.Char(string="Category Name", required=True)
    description = fields.Char(string="Description", required=True)