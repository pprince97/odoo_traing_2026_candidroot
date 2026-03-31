from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class LibraryBooks(models.Model):
    _name = 'library.books'
    _description = 'Library Books'

    name = fields.Char(string='Book Name',required=True)
    barcode = fields.Char(string='Barcode',required=True)
    description = fields.Text(string='Description')
    currency = fields.Many2one('res.currency',string='Currency')
    state = fields.Selection([('unpublished','Unpublished'),('published','Published')],string='state',default='unpublished')
    category = fields.Char(string='Category')
    available_copies = fields.Integer(string='Available Copies',readonly=True)
    stock = fields.Integer(string='Stock',required=True)
    cover_image = fields.Image(string='Cover Image')
    borrow_price = fields.Float(string='Borrow Price (per day)',required=True)
    maximum_day_limit = fields.Integer(string='Maximum Days Limit',required=True)
    available_copies_btn = fields.Char(string='Available Copy',compute='_compute_available_copies')
    borrow_request_line_ids = fields.One2many('library.borrow.request.lines','book_id',string='Borrow History')
    borrow_history_count = fields.Integer(string='Borrow History Cnt',compute='_compute_history_count')
    genre_ids = fields.Many2many('library.books','book_genre_rel','book_id','genre_id')
    history_ids = fields.One2many('library.image.history','book_id',string='History')

    def book_state_issued(self):
        self.state = 'published'

    def book_state_unpublished(self):
        self.state = 'unpublished'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(LibraryBooks,self).create(vals_list)
        for book in res:
            book.available_copies = book.stock
            if book.barcode and self.env['library.books'].search([('id','!=',book.id),('barcode','=',book.barcode)]):
                raise ValidationError(_("2 Books cannot have same barcode"))
        return res

    def write(self, vals):
        res = super(LibraryBooks, self).write(vals)
        for rec in self:
            if rec.cover_image:
                self.env['library.image.history'].create({'book_id': rec['id'],'images': rec['cover_image']})
        return res

    @api.depends('available_copies','stock')
    def _compute_available_copies(self):
        for book in self:
            book.available_copies_btn = "" + str(book.available_copies) + " / "+  str(book.stock)

    def available_copies_btn1(self):
        return None

    @api.depends('borrow_request_line_ids')
    def _compute_history_count(self):
        for book in self:
            book.borrow_history_count = len(book.borrow_request_line_ids)

    def redirect_borrow_request_lines(self):
        return{
            'name': 'History',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request.lines',
            'view_mode': 'list,form',
            'domain': [('book_id', 'in', self.id)],
            'target': 'current',
        }