from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _order = 'name, id'


    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer(string='Color')