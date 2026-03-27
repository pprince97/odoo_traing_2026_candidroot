from odoo import models, fields, api


class Librarian(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='phone')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],)

    # member = fields.Selection(
    #     selection_add=[('student', 'Student'), ('librarian', 'Librarian')],
    #     string="Member"

    def action_view_borrow_history(self):
        return {
            'name': 'Borrow History',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow_request.borrow_request',
            'view_mode': 'list,form',
            'domain': [('librarian_id', '=', self.id)],
            'target': 'new',
        }