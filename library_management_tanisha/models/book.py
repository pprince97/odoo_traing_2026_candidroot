from odoo import models,fields,api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Books'

    name = fields.Char(string='Name',required=True)
    barcode = fields.Char(string='Barcode',required=True)
    description = fields.Text(string='Description')
    currency_id = fields.Many2one(comodel_name='res.currency',string="Foreign Currency")
    state = fields.Selection([('published', 'Published'),('unpublished', 'Unpublished')],string='State',default='published')
    category = fields.Selection([('knowledge', 'Knowledge'),('novel', 'Novel'),('story', 'Story'),('science', 'Science'),('history', 'History'),('comic','Comic')],string='Category',default='knowledge')
    stock = fields.Integer(string='Stock')
    available_copies = fields.Integer(string='Available copies',compute='_compute_available_copies')
    cover_image = fields.Image(string='Cover Image')
    borrow_price = fields.Monetary(store=True, readonly=False,currency_field='currency_id',string='Borrow Price (per day)',required=True)
    max_day_limit = fields.Integer(string='Maximum Day Limit')
    borrow_request_line_ids = fields.One2many(comodel_name='library.borrow.request.lines',inverse_name='book_id')
    borrow_history_ids = fields.Many2many(comodel_name='book.history.wizard', relation='book_borrow_history_rel', column1='book_id', column2='book_borrow_id', string='Borrow Books')
    available_copies_string = fields.Char()

    def _compute_available_copies(self):
        for book in self:
            borrow_request_lines = self.env['library.borrow.request.lines'].search([('book_id','in',self.ids),('borrow_request_id.state','=','issued')])
            total = 0
            for rec in borrow_request_lines:
                if rec.book_id.id == book.id:
                    total += rec.quantity
                else:
                    continue
            book.available_copies = book.stock - total
            book.available_copies_string = str(book.available_copies) + " / " + str(book.stock)

    def history_borrowed(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('borrow_request_line_ids.book_id','=',self.id)],
        }
