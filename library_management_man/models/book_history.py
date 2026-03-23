from odoo import models, fields, api

class BookHistory(models.Model):
    _name = 'book.history'
    _description = 'Book History'

    file_name = fields.Char(string='File Name')
    file = fields.Image(string='File')
    upload_date = fields.Datetime(string='Upload Date')

    book_id = fields.Many2one('library.book', string='Book')
