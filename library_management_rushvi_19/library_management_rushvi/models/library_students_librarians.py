from odoo import models,fields,api
from odoo.exceptions import UserError

class LibraryStudentsLibrarian(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender",default='male')

    # student related fields
    is_student = fields.Boolean('Student')
    borrow_request_student_ids = fields.One2many('library.borrow.requests','student_id',string="Borrow History Student")
    borrow_request_student_count = fields.Integer(string="Borrow Count", compute='_compute_student_count')

    # LIBRARIAN RELATED FIELDS
    is_librarian = fields.Boolean('Librarian')
    borrow_request_librarian_ids = fields.One2many('library.borrow.requests', 'librarian_id', string="Borrow History Librarian")
    borrow_request_librian_count = fields.Integer(string="Borrow History Count", compute='_compute_librarian_count')


    @api.model_create_multi
    def create(self, vals_list):
        res = super(LibraryStudentsLibrarian, self).create(vals_list)
        for rec in res:
            user = {
                'name': rec.name,
                'email': rec.email,
                'login': rec.email,
                'password': rec.email,
                'group_ids':[],
                'partner_id': rec.id,
            }
            group_student = self.env.ref('library_management_rushvi.group_library_student')
            group_librarian = self.env.ref('library_management_rushvi.group_library_librarian')
            group_librarian_menu = self.env.ref('library_management_rushvi.res_groups_privilege_library_menu')
            if rec.is_student:
                user['group_ids'] = [(6,0,[ group_student.id])]
            elif rec.is_librarian:
                user['group_ids'] = [(6, 0, [group_librarian_menu.id, group_librarian.id,self.env.ref('base.group_erp_manager').id]),
                                 self.env.ref('base.group_partner_manager').id]

            user = self.env['res.users'].create(user)
            rec.user_id = user.id
        return res

    @api.depends('borrow_request_student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.borrow_request_student_count = len(rec.borrow_request_student_ids)

    def view_borrow_requests_students(self):
        return {
            'name': 'History',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.requests',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'target': 'current',
        }

    @api.depends('borrow_request_librarian_ids')
    def _compute_librarian_count(self):
        for rec in self:
            rec.borrow_request_librian_count = len(rec.borrow_request_librarian_ids)

    def view_borrow_requests_librarians(self):
        return {
            'name': 'Borrow History',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.requests',
            'view_mode': 'list,form',
            'domain': [('librarian_id', '=', self.id)],
            'target': 'current',
        }

