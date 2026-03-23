from odoo import models, fields, api, Command


class LibraryStudent(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    is_student = fields.Boolean()
    borrow_request_ids = fields.One2many(comodel_name='library.borrow.request', inverse_name='student_id',
                                         string='Borrow Requests')
    book_history_id = fields.Many2many(comodel_name='book.history.wizard', relation='book_student_rel',
                                       column1='student_id', column2='book_borrow_id', string='Book Borrow history')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(LibraryStudent, self).create(vals_list)
        for rec in res:
            record = self.env['res.users'].create({
                'partner_id': rec.id,
                'name': rec.name,
                'email': rec.email,
                'phone': rec.phone,
                'login': rec.name,
                'password': rec.email,
                'group_ids': [Command.set([self.env.ref('library_management_tanisha.group_library_student').id])],
            })
            if rec.is_librarian:
                record['group_ids'] = [Command.set([self.env.ref('library_management_tanisha.group_library_librarian').id])]
        return res

    def borrowed_book_history(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }
