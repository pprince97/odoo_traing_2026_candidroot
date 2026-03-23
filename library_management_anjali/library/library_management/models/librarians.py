from odoo import models,fields,api

class Librarians(models.Model):
    _inherit = 'res.partner'

    librarian_code = fields.Char(string='Librarian Code',readonly=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')

    librarian_borrow_count = fields.Integer(string='Librarian Borrow Count',compute='_compute_librarian_borrow_count')


    @api.model_create_multi
    def create(self, vals):
        res = super(Librarians, self).create(vals)
        for rec in res:
            if self.env.context.get('librarian') and not rec.librarian_code:
                rec.librarian_code = self.env['ir.sequence'].next_by_code('librarian.sequence') or 'New'
                librarian_group = self.env.ref('library_management.group_project_librarian')
                librarian_group_menu = self.env.ref('library_management.group_project_librarian_menu')
                user = self.env['res.users'].create({
                    'name': rec.name,
                    'email': rec.email,
                    'login': rec.email,
                    'password': rec.email,
                    'group_ids': [(4, librarian_group.id),(4, librarian_group_menu.id)],
                    'partner_id': rec.id,
                })
                rec.user_id = user.id
        return res

    def _compute_librarian_borrow_count(self):
        for rec in self:
            rec.librarian_borrow_count = self.env['library.borrow.request'].search_count([('librarian_id','=',rec.id)])

    def librarian_borrow_request(self):
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('librarian_id','=',self.id)],
            'target': 'self',
        }
