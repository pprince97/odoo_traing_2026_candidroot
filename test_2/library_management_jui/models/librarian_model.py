from odoo import fields,models,api,Command

class LibrarianModel(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    is_librarian = fields.Boolean(string='Is Librarian')

    borrow_request_count = fields.Integer(string='Borrow Request Count')

    @api.model_create_multi
    def create(self, vals):
        res = super(LibrarianModel, self).create(vals)
        for rec in res:
            if rec and rec.is_librarian == True:
                user = self.env['res.users']
                user_id = user.create(
                    {'name': rec.name, 'login': rec.name, 'email': rec.email, 'partner_id': rec.id, 'password': 'admin',
                     'group_ids':[Command.set([self.env.ref('library_management_jui.library_group_librarian').id,self.env.ref('library_management_jui.library_group_librarian_librarian').id])]})
                rec.update({'user_id': user_id.id})
        return res

    def borrow_request_by_librarian(self):
        borrow_request = self.env['library.borrow.request']
        self.borrow_request_count = borrow_request.search_count([
            ("librarian_id", "=", self.id),
        ])
        return {
            'name': "Borrow Request",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'library.borrow.request',
            'target': 'self',
            'domain': [
                ("librarian_id", "=", self.id),
            ],
        }