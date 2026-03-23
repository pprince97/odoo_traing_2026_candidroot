from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class Books(models.Model):
    _name = 'library.books'
    _description = 'Library Books'

    name = fields.Char(string='Name', required=True)
    barcode = fields.Char(string='Barcode', required=True)
    description = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency',string='Currency')
    borrow_price = fields.Monetary(string='Borrow Price',currency_field='currency_id',required=True)
    state = fields.Selection([('published','Published'),('unpublished','Unpublished')],string='State',default='unpublished')
    available_copies = fields.Integer(string='Available Copies', readonly=True)
    stock = fields.Integer(string='Stock')
    cover_image = fields.Image(string='Cover Image')
    maximum_day =fields.Integer(string='Maximum Day')

    book_borrow_count = fields.Integer(string='Book Borrow Count',compute='_compute_book_borrow_count')
    available_book_count = fields.Char(string='Available Book Count',compute='_compute_available_book')

    def published_books(self):
        self.update({'state': "published"})

    def unpublished_books(self):
        self.update({'state': "unpublished"})

    def _compute_book_borrow_count(self):
        for rec in self:
            rec.book_borrow_count = self.env['library.borrow.request'].search_count([('borrow_request_ids.book_id','=',rec.id)])

    def book_borrow_request(self):
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('borrow_request_ids.book_id','=',self.id)],
            'target': 'self',
        }

    @api.depends('available_copies','stock')
    def _compute_available_book(self):
        for rec in self:
            rec.available_book_count = str(rec.available_copies) + "/" + str(rec.stock)

    def available_book(self):
        return None

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Books,self).create(vals_list)
        for rec in res:
            rec.available_copies = rec.stock
            if rec.barcode and self.env['library.books'].search([('id','!=',rec.id),('barcode','=',rec.barcode)]):
                raise ValidationError(_("Any books cannot have same barcode"))
        return res

