from odoo import models, fields, api, Command

from odoo.exceptions import ValidationError


class Librarian(models.Model):
    _inherit = 'res.partner'

    library_role = fields.Selection([('student', 'Student'), ('librarian', 'Librarian')], string="Library Role")
    librarian_borrow_request_count = fields.Integer(string="Number of Borrow Requests",
                                                    compute="_compute_librarian_borrow_request_count")

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        # import pdb;
        # pdb.set_trace()
        for rec in res:
            if rec and rec.library_role == 'librarian':
                user = self.env['res.users'].create(
                    {'name': rec.name,
                     'email': rec.email,
                     'partner_id': rec.id,
                     'login': rec.name,
                     'password': rec.name,
                     'group_ids': [
                         Command.set([self.env.ref('library_management_urvi.group_library_librarian').id,
                                      self.env.ref('library_management_urvi.group_library_hide_librarian').id])]})
                rec.write({'user_id':user.id})
                # rec.user_id = user.id
            if rec and rec.library_role == 'student':
                user = self.env['res.users'].create(
                    {'name': rec.name,
                     'email': rec.email,
                     'partner_id': rec.id,
                     'login': rec.name,
                     'password': rec.name,
                     'group_ids': [
                         Command.set([self.env.ref('library_management_urvi.group_library_student').id])]})
                rec.write({'user_id':user.id})
                # rec.user_id = user.id
        return res


    def _compute_librarian_borrow_request_count(self):
        self.librarian_borrow_request_count = self.env['library.borrow.request'].search_count(
            [('librarian_id', 'in', self.ids)])


    def show_librarian_borrow_request(self):
        a = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('librarian_id', '=', self.id)],
            'target': 'self'
        }
        if self.borrow_request_count == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['library.borrow.request'].search(
                [('librarian_id', '=', self.id)])).id
        return a
