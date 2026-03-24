from odoo import fields,models,api,Command

class StudentModel(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    is_student = fields.Boolean(string='Is Student')

    borrow_history_count = fields.Integer(string='Borrow History Count')

    @api.model_create_multi
    def create(self, vals):
        res = super(StudentModel, self).create(vals)
        for rec in res:
            if rec and rec.is_student == True:
                user = self.env['res.users']
                user_id = user.create(
                    {'name': rec.name, 'login': rec.name, 'email': rec.email, 'partner_id': rec.id, 'password': 'admin',
                     'group_ids':[Command.set([self.env.ref('library_management_jui.library_group_student').id])]})
                rec.update({'user_id': user_id.id})
        return res

    def borrow_history_of_student(self):
        borrow_history = self.env['library.borrow.request']
        self.borrow_history_count = borrow_history.search_count([
            ("student_id", "=", self.id),
        ])
        return {
            'name': "Borrow History",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'library.borrow.request',
            'target': 'self',
            'domain': [
                ("student_id", "=", self.id),
            ],
        }