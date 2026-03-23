from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = "res.users"

    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ],string='Gender')
    is_student = fields.Boolean(string='Is Student')
    book_borrowed_count = fields.Char(string='Book Borrowed Count',
                                      compute="_compute_book_borrowed_count")

    def _compute_book_borrowed_count(self):
        for rec in self:
            rec.book_borrowed_count = self.env['library.book.borrow'].search_count([
            ('student_id.id', '=', self.id)])

    def action_book_borrowed_history(self):
        self.ensure_one()
        return {
            'name': 'Book Borrowed History',
            'type': 'ir.actions.act_window',
            'res_model': 'library.book.borrow',
            'view_mode': 'list,form',
            'domain': [('student_id.id', '=', self.id)],
            }