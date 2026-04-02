from odoo import models, fields, api, Command


class LibraryLibrarian(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    is_librarian = fields.Boolean()
    borrow_request_ids = fields.One2many(comodel_name='library.borrow.request', inverse_name='librarian_id',
                                         string='Borrow Requests')
    password = fields.Char(string='Password')

    def borrowed_requests(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('librarian_id', '=', self.id)],
        }

