from odoo import fields,models,api

class Librarian(models.Model):
    _inherit = 'res.partner'

    person = fields.Selection([
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    ])
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ],string='Gender',default='male')
    request_processed = fields.Integer(compute='_compute_request_processed')


    def _compute_request_processed(self):
        count = self.env['library.borrow.request'].search_count([('librarian_id','=',self.id)])
        self.request_processed = count


    def borrow_requests_processed(self):
        self.ensure_one()
        if self.request_processed == 1:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'library.borrow.request',
                'view_mode': 'form',
                'res_id': self.id,
                'domain': [('librarian_id', '=', self.id)],
                'context': {'form_view_ref': 'library_management.borrow_request_view_form'}
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'library.borrow.request',
                'view_mode': 'list,form',
                'domain': [('librarian_id', '=', self.id)],
                'context': {'list_view_ref': 'library_management.borrow_request_list_form',
                            'form_view_ref': 'library_management.borrow_request_view_form'}
            }


    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('default_person') == 'librarian':
            for vals in vals_list:
                vals['person']='librarian'
        return super().create(vals_list)

    # 3. Librarians
    # Fields:
    # Name(required)
    # Email(required)
    # Phone
    # Gender
    # Business Rules:
    # Only Admin can create Librarian not any other User
    # Smart Buttons
    # For Showing How many Borrow Request Process By Librarian