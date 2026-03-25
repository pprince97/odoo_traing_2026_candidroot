from odoo import fields, models, api


class Student(models.Model):
    _inherit = 'res.partner'

    # person = fields.Selection([
    #     ('student', 'Student'),
    #     ('librarian', 'Librarian'),
    # ])
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')
    books_borrow_history = fields.Integer(string='Books borrow history',compute='_compute_books_borrow_history')

    def _compute_books_borrow_history(self):
        for record in self:
            record.books_borrow_history = self.env['library.borrow.request'].search_count([('student_id', '=', record.id)])


    def show_book_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)]
            # 'context': {'list_view_ref': 'library_management.borrow_request_list_form',
            #             'form_view_ref': 'library_management.borrow_request_view_form'}
        }

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('default_person') == 'student':
            for vals in vals_list:
                vals['person'] = 'student'
        return super().create(vals_list)

    # 2.
    # Students
    # Fields:
    # Name(required)
    # Email(required)
    # Phone
    # Gender
    # Business Rules:
    # ●​ Smart Button in Form View For Showing History of Book Borrowed by Student
    # ●​ Students have no Rights to See any smart Buttons, Only Librarian and Admin can see Book Borrow History From Smart Buttons.
    # ●​ Students only can see Borrow Requests.Students shouldn’t see any other menu.
