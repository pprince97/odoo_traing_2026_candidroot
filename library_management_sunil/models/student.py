from odoo import models, fields, api


class Student(models.Model):
    _inherit = 'res.partner'


    member = fields.Selection([('librarian', 'Librarian'), ('student', 'Student')], string="Member")

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='phone')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])

    borrow_count = fields.Integer(string="Borrowed Books", compute="_compute_borrow_count")

    def _compute_borrow_count(self):
        for rec in self:

            if rec.member == 'student':
                rec.borrow_count = self.env['borrow_request.borrow_request'].search_count([
                    ('student_id', '=', rec.id)
                ])

            elif rec.member == 'librarian':
                rec.borrow_count = self.env['borrow_request.borrow_request'].search_count([
                    ('librarian_id', '=', rec.id)
                ])

            else:
                rec.borrow_count = 0


    def action_view_borrow_history_student(self):
        self.ensure_one()
        return {
            'name': 'Borrow History',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow_request.borrow_request',
            'view_mode': 'list,form',
            'domain': [
                ('student_id', '=', self.id),
            ],
        }
