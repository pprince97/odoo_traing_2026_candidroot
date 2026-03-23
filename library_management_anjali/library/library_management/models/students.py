from odoo import models,fields,api

class Students(models.Model):
    _inherit = 'res.partner'

    student_code = fields.Char(string='Student Code',readonly=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')

    student_borrow_count = fields.Integer(string='Student Borrow Count',compute='_compute_student_borrow_count')

    @api.model_create_multi
    def create(self, vals):
        res = super(Students, self).create(vals)
        for rec in res:
            if self.env.context.get('student') and not rec.student_code:
                rec.student_code = self.env['ir.sequence'].next_by_code('student.sequence') or 'New'
                student_group = self.env.ref('library_management.group_project_student')
                user = self.env['res.users'].create({
                    'name': rec.name,
                    'email': rec.email,
                    'login': rec.email,
                    'password': rec.email,
                    'group_ids': [(4, student_group.id)],
                    'partner_id': rec.id,
                })
                rec.user_id = user.id
        return res

    def _compute_student_borrow_count(self):
        for rec in self:
            rec.student_borrow_count = self.env['library.borrow.request'].search_count([('student_id','=',rec.id)])

    def student_borrow_request(self):
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('student_id','=',self.id)],
            'target': 'self',
        }
