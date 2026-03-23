from odoo import models,fields,api

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    student_id = fields.Many2one('school.student',string='Student ID')
    student_address = fields.Char(string="Student Address")
    student_roll_no = fields.Integer(string="Student Roll No")
    student_dob = fields.Date(string="Student Date of Birth")
    subject_ids = fields.Many2many('school.subject','res_partner_inherit_rel','res_partner_id','subject_id','Subjects')

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['student_address']='addresssssss'
        res = super(ResPartnerInherit, self).create(vals)
        return res

    def write(self, vals):

        if vals and vals.get('student_roll_no'):
            vals['student_roll_no']='222'
        res = super(ResPartnerInherit, self).write(vals)
        # print(val)
        return res
