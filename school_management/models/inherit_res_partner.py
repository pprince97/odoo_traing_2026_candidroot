from odoo import models,fields,api

class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    student_id = fields.Char(string='Student ID')
    student_address = fields.Text(string='Student Address')
    student_roll_no = fields.Integer(string='Student Roll No')
    student_dob = fields.Date(string='Student DOB')
    subject_ids = fields.Many2many('school.subject','inherit_sub_rel','respartner_id','subject_id')

    # @api.model_create_multi
    # def create(self, vals):
    #     # for val in vals:
    #     #     val['student_id'] = val['student_id'].upper()
    #     res = super(InheritResPartner, self).create(vals)
    #     return res

    # def write(self, vals):
    #     # print('write>>>>>>', vals)
    #     # for val in vals:
    #     # if vals and vals.get('student_address'):
    #     #     vals['student_address'] = vals['student_address'].capitalize()
    #     res = super(InheritResPartner, self).write(vals)
    #     return res
