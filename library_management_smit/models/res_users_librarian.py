from odoo import models, fields, api, Command

class ResUsers(models.Model):
    _inherit = "res.users"

    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ],string='Gender')
    is_student = fields.Boolean(string='Is Student', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('librarian'):
            group_lib_id = self.env.ref(
                'library_management_smit.library_group_librarian'
            ).id
            group_creation_id = self.env.ref(
                'base.group_partner_manager'
            ).id
            group_erp_manager_id = self.env.ref(
                'base.group_erp_manager'
            ).id

            for vals in vals_list:
                vals['is_student'] = False
                vals['login'] = vals['email']
                vals['password'] = vals['login']
                vals['group_ids'] = [Command.link(group_lib_id),
                                     Command.link(group_creation_id),
                                     Command.link(group_erp_manager_id)
                                     ]
        elif self.env.context.get('student'):
            group_student_id = self.env.ref(
                'library_management_smit.library_group_student'
            ).id

            for vals in vals_list:
                vals['is_student'] = True
                vals['login'] = vals['email']
                vals['password'] = vals['login']
                vals['group_ids'] = [Command.link(group_student_id)]
        return super().create(vals_list)

