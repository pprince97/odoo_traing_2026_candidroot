from odoo import fields,models,api,Command

class Student(models.Model):
    _inherit = "res.partner"

    gender = fields.Selection([('male','male'),('female','female')],string="Gender",default='male')
    borrow_request_count = fields.Integer(string="Borrow Request Count",compute="_compute_borrow_request_count")

    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Student, self).create(vals)
    #     for rec in res:
    #         if rec and rec.library_role == 'student':
    #             user = self.env['res.users'].create(
    #                 {'name': rec.name,
    #                  'email': rec.email,
    #                  'partner_id': rec.id,
    #                  'login': rec.name,
    #                  'password': rec.name,
    #                  'signature': rec.name,
    #                  'group_ids': [
    #                      Command.set([self.env.ref('library_management_urvi.group_library_student').id])]})
    #             rec.user_id = user.id
    #     return res

    def _compute_borrow_request_count(self):
        self.borrow_request_count = self.env['library.borrow.request'].search_count([('student_id','=',self.id)])

    def show_borrow_request(self):
        a = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'target': 'self'
        }
        if self.borrow_request_count == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['library.borrow.request'].search(
                [('student_id', '=', self.id)])).id
        return a

    def action_students(self):
        if self.env.user.has_group('library_management_urvi.group_library_student'):
            action = self.env['ir.actions.act_window']._for_xml_id(
                'library_management_urvi.student_action_student')
            return action
        else:
            action = self.env['ir.actions.act_window']._for_xml_id(
                'library_management_urvi.student_action')
            return action