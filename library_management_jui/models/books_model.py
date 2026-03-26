from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class BooksModel(models.Model):
    _name = 'library.books'
    _description = 'Books'

    name = fields.Char(string='Name', required=True)
    barcode = fields.Char(string='Barcode',required=True)
    description = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency')
    state = fields.Selection([('published', 'Published'), ('unpublished', 'Unpublished')],string='State',default='unpublished')
    category = fields.Selection([('novel', 'Novel'), ('comic', 'Comic'), ('religious', 'Religious'), ('fashion', 'Unpublished'), ('educational', 'Educational'), ('philosophical', 'Philosophical')],string='Category')
    available_copies = fields.Integer(string='Available copies',compute='_compute_available_copies')
    stock = fields.Integer(string='Stock')
    stock_copy = fields.Integer(string='Stock Copy')
    cover_image = fields.Image(string='Cover Image',attachment=True)
    borrow_price = fields.Float(string='Borrow Price (per day)',required=True)
    maximum_day_limit = fields.Integer(string='Maximum Day Limit')

    borrowed_count = fields.Integer(string='Borrowed Count')

    def _compute_available_copies(self):
        for rec in self:
            if rec:
                not_available = self.env['library.borrow.request.lines'].search(
                    [('book_id', '=', rec.id), ('borrow_request_id.state', '=', 'issued')])
                not_available_count = 0
                for i in not_available:
                    if i.quantity:
                        not_available_count += i.quantity
                rec.available_copies = rec.stock - not_available_count

    @api.onchange('stock')
    def onchange_stock(self):
        for rec in self:
            rec['available_copies'] += (rec['stock'] - rec['stock_copy'])
            rec['stock_copy'] = rec['stock']

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if self.env['library.books'].search([('barcode','=',rec['barcode'])]):
                raise ValidationError(_("Barcode must be unique"))
            rec['stock_copy'] = rec['stock']
        res = super(BooksModel, self).create(vals)
        return res

    def write(self, vals):
        res = super(BooksModel, self).write(vals)
        for rec in self:
            if rec.cover_image:
                self.env['library.book.history'].create({'book_id':rec['id'],'image':rec['cover_image']})
        return res

    def history_of_borrowed(self):
        borrow_history = self.env['library.borrow.request.lines']
        self.borrowed_count = borrow_history.search_count([
            ("book_id", "=", self.id),
        ])
        return {
            'name': "Borrow History",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'library.borrow.request.lines',
            'target': 'self',
            'domain': [
                ("book_id", "=", self.id),
            ],
        }
