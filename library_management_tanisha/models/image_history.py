from odoo import models,fields,api

class HistoryField(models.Model):
    _name = 'library.image.history'
    _description = 'Image History'

    book_id = fields.Many2one(comodel_name='library.book')
    history_image = fields.Image(string='Image')
