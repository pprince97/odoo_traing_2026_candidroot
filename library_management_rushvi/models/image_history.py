from odoo import models,fields,api,_

class HistoryButton(models.Model):
    _name = 'library.image.history'
    _description = 'History Button'

    images = fields.Image(string='Images')
    book_id = fields.Many2one('library.books')