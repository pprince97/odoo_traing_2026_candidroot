from odoo import models, fields, api

class LibraryStudent(models.Model):
    _inherit = 'res.partner'

    student_code = fields.Char(string="Student Code",readonly=True)
    gender = fields.Selection([('male','male'),('female','female')],string='Gender')
    request_ids = fields.One2many('library.borrow.request', 'student_id', string='Borrow Requests')
    borrow_request_line_ids = fields.One2many('library.borrow.request.line', 'student_id', string='Borrow Requests')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if self.env.context.get('is_student') == 'student':
                val['student_code'] = self.env['ir.sequence'].next_by_code('student.sequence') or 'UnKnown'
        res = super().create(vals_list)
        return res

    def history_of_borrow_book(self):
        self.ensure_one()
        return {
            'name': "Book Borrow History",
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request.line',
            'view_mode': 'list,form',
            'target': 'Current',
            'domain': [('student_id', '=', self.id)],
        }
