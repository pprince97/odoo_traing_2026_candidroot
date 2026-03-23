from odoo import models,fields

class ImageHistory(models.Model):
    _name = 'library.image.history'
    _description = 'Library Image History'

    book_id = fields.Many2one('library.book',string='Book')
    history_image = fields.Image(string="Image")