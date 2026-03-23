from odoo import model,fields,api

class Genre(models.Model):
    _name = 'library.genre'
    _description = 'Genre'

    name = fields.Char(string='Name')
    book_ids = fields.Many2many('library.books','book_genre_rel','genre_id','book_id')