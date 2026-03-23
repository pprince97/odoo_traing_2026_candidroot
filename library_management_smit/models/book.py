from odoo import models, fields, api
from datetime import datetime


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string='Book Name', required=True)
    barcode = fields.Char(string='Barcode', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.EUR'))
    description = fields.Char(string='Description')
    state = fields.Selection([('published', 'Published'), ('unpublished', 'Unpublished')], string='State',
                             default='unpublished')
    category_ids = fields.Many2many('library.book.category', 'book_category_rel', 'book_id', 'category_id',
                                    string='Category')
    available_copies = fields.Integer(string='Available Copies', compute='_compute_available_copies_count')
    stock = fields.Integer(string='Stock', required=True)
    cover_image = fields.Image(string='Cover Image', widget="custom_image")
    filename = fields.Char(string='File Name', tracking=True)
    borrow_price = fields.Float(string='Borrow Price Per Day', required=True)
    max_day_limit = fields.Integer(string='Max Day Limit')
    book_image_history_ids = fields.One2many('book.image.history', 'book_id', string='History')

    available_books_count = fields.Char(string='Book Count',
                                        compute="_compute_available_book_count"
                                        )
    book_borrowed_count = fields.Integer(string='Book Borrowed Count',
                                         compute="_compute_book_borrowed_count"
                                         )
    fine_amount = fields.Integer(
        compute="_compute_fine_amount"
    )

    def _compute_book_borrowed_count(self):
        for rec in self:
            rec.book_borrowed_count = self.env['library.book.borrow'].search_count([
                ('borrow_req_ids.book_id.id', '=', self.id)])

    def _compute_available_copies_count(self):
        for rec in self:
            if rec:
                not_available = self.env['library.book.borrow.lines'].search(
                    [('book_id', 'in', rec.ids), ('borrow_req_id.state', '=', 'issued')])
                not_available_count = 0
                for i in not_available:
                    if i.quantity:
                        not_available_count += i.quantity
                rec.available_copies = rec.stock - not_available_count

    def _compute_fine_amount(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'library_management_smit.fine_amount'
        )

        for rec in self:
            rec.fine_amount = param

    def action_borrowed_history(self):
        self.ensure_one()
        for rec in self:
            if rec.book_borrowed_count > 1:
                return {
                    'name': 'Borrowed History',
                    'type': 'ir.actions.act_window',
                    'res_model': 'library.book.borrow',
                    'view_mode': 'list,form',
                    'domain': [('borrow_req_ids.book_id', '=', self.id)],
                }
            elif rec.book_borrowed_count <= 1:
                return {
                    'name': 'Borrowed History',
                    'type': 'ir.actions.act_window',
                    'res_model': 'library.book.borrow',
                    'view_mode': 'form',
                    'target': 'current',
                    'domain': [('borrow_req_ids.book_id', '=', self.id)],
                }
        return True

    def action_custom_image_logic(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Image History',
            'res_model': 'book.image.history',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'target': 'new',
        }

    def _compute_available_book_count(self):
        for rec in self:
            rec.available_books_count = f"{self.available_copies} / {self.stock}"

    def write(self, vals):
        res = super().write(vals)
        self.env['book.image.history'].create({
            'book_id': self._origin.id,
            'image': self.cover_image,
            'name': self.filename,
            'change_date': datetime.now(),
        })
        return res

    def action_book_history(self):
        self.ensure_one()
        return {
            'name': 'Book History',
            'type': 'ir.actions.act_window',
            'res_model': 'book.image.history',
            'view_mode': 'list',
            'target': 'new',
            'domain': [('book_id', '=', self.id)],
        }


class BookImageHistory(models.Model):
    _name = 'book.image.history'
    _description = 'Book Image History'

    book_id = fields.Many2one('library.book', 'Book')
    image = fields.Image(string='Image Size')
    name = fields.Char(string='Image Name')
    change_date = fields.Datetime(string='Change Date')
