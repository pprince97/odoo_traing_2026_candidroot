from odoo import models,fields,api,_

class ImageHistory(models.Model):
    _name = 'library.image.history'
    _description = 'Image History'

    image = fields.Image(string='Image')
    book_id = fields.Many2one('library.books', string='Book')
