from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = 'book.book'
    _description = 'book'
    _rec_name = 'name'



    name = fields.Char(required=True)
    barcode = fields.Char()
    description = fields.Char()
    currency_id = fields.Many2one('res.currency')
    state = fields.Selection([
        ('published', 'Published'),('unpublished', 'Unpublished')])
    category_id = fields.Many2one('book.category', string="Category")
    available_copies= fields.Integer(string='Available Copies')
    stock = fields.Integer(string='Stock')
    cover_image = fields.Image(string='Cover Image')
    borrow_price_per_day = fields.Integer(string='Borrow Price', required=True)
    maximum_day_limit = fields.Integer(string='Maximum Days Limit')
    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user)

    def action_publish(self):
        for rec in self:
            rec.state = 'published'

    def action_unpublish(self):
        for rec in self:
            rec.state = 'unpublished'

    borrowed_count = fields.Integer(string="Borrowed Count", compute="_compute_borrowed_count")

    def _compute_borrowed_count(self):
        for rec in self:
            count = self.env['borrow_request.borrow_request'].search_count([
                ('book_id', '=', rec.id)
            ])
            rec.borrowed_count = count

    available_display = fields.Char(string="Available Books",compute="_compute_available_display")

    @api.depends('available_copies', 'stock')
    def _compute_available_display(self):
        for rec in self:
            available = rec.available_copies or 0
            stock = rec.stock or 0
            rec.available_display = f"{available} / {stock}"

    @api.constrains('available_copies', 'stock')
    def _check_available_copies(self):
        for rec in self:
            if rec.available_copies > rec.stock:
                raise ValidationError("Available copies cannot be greater than total stock.")

    def action_view_borrow_history(self):
        return {
            'name': 'Borrow History',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow_request.borrow_request',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'target': 'current',
        }






