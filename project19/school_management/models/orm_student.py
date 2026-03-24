from odoo import models, fields,api

class OrmStudent(models.Model):
    _inherit='res.partner'

    name = fields.Char(string='Name')
    student_id = fields.Integer(string='Student Id')
    roll_n= fields.Integer(string='Roll number')
    address = fields.Text(string='Address')
    dob = fields.Date(string='Date Of Birth')

    subject_ids=fields.Many2many('sale.order','orm_subject_student_rel','student_ids','subject_ids',string='Subjects')

    @api.model_create_multi
    def create(self,vals):
        for val in vals:
            val['student_id']='1'
        res = super(OrmStudent,self).create(vals)
        return res

    def write(self,vals):
        print(vals)
        if vals and vals.get('roll_n'):
            vals['roll_n'] = vals['roll_n']+1
        res = super(OrmStudent,self).write(vals)
        return res