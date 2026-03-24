from odoo import fields, models, api

class Students(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ],
        string='Gender',
        default='male'
    )

    member = fields.Selection([('student', 'Student'), ('librarian', 'Librarian')], string="Member")

    borrow_request_lines_ids = fields.One2many('library.borrow.request', 'student_id', string='Borrow Requests')

    count_total_book = fields.Integer(string='Total Books', compute='get_history_of_books')

    def get_history_of_books(self):
        self.ensure_one()

        self.count_total_book = self.env['library.borrow.request'].search_count([('student_id', '=', self.id)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'History of borrowed books',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [
                ('student_id', '=', self.id),
            ],

        }

    @api.model
    def default_get(self, fields_list):
        # 1. Get default values from parent/super
        res = super(Students, self).default_get(fields_list)

        # 2. Add dynamic logic
        if self.env.user.has_group('base.group_user'):
            res['comment'] = 'Default comment for internal users'

        # 3. Return the updated dictionary
        print("============================>", res)
        return res