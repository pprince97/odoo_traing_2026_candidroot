from odoo import models, fields, api

class LibraryLibrarian(models.Model):
    _inherit = 'res.partner'

    librarian_code = fields.Char(string="Library Code",readonly=True)
    gender = fields.Selection([('male','male'),('female','female')],string='Gender')
    request_ids = fields.One2many('library.borrow.request', 'librarian_id', string='Requests')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if self.env.context.get('is_librarian') == 'librarian':
                val['librarian_code'] = self.env['ir.sequence'].next_by_code('librarian.sequence') or 'UnKnown'
        res = super().create(vals_list)
        return res

    def borrow_request(self):
        self.ensure_one()
        return {
            'name': "Book Borrow Request",
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'target': 'Current',
            'domain': [('librarian_id', '=', self.id)],
        }




