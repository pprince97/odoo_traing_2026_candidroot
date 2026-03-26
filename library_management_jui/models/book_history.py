from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class BookHistoryModel(models.Model):
    _name = 'library.book.history'
    _description = 'Book History'

    book_id = fields.Many2one('library.books',string='Books')
    image = fields.Image(string='Image')
