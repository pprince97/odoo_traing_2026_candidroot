from odoo import fields, models, api

class Librarian(models.Model):
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

    count_total_request = fields.Integer(string='Total Requests', compute='get_borrow_request')

    def get_borrow_request(self):
        self.ensure_one()

        self.count_total_request = self.env['library.borrow.request'].search_count([('librarian_id', '=', self.id)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Total borrowed request',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [
                ('librarian_id', '=', self.id),
            ],
        }