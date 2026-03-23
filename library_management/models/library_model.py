from odoo import models,fields

class Library(models.Model):
    _name = 'library.library'
    _description = 'Library Model'
    _rec_name = 'library_name'

    library_name = fields.Char(string="Library Name")
    address = fields.Text(string="Address")
    available_books = fields.Integer(string="Available Books")
