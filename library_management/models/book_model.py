from odoo import models,fields

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book Model Description'
    _rec_name = 'book_name'

    book_name = fields.Char(string='Book Name')
    currency_id = fields.Many2one('res.currency', string='Currency')
    book_price = fields.Monetary(string='Book Price')
    stock_quantity = fields.Integer(string='Stock Quantity')
    release_date = fields.Date(string='Release Date')
    no_of_pages = fields.Integer(string='No of Pages')
    genre = fields.Selection([('mystery','Mystery'),('horror','Horror'),('romantic','Romantic'),('science','Science'),('history','History'),('biography','Biography')],string='Genre')
    description = fields.Text(string='Description')
    cover = fields.Image(string='Cover Image')
