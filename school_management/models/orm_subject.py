from odoo import models, fields,api

class OrmSubject(models.Model):
    _inherit='sale.order'

    subject_id = fields.Integer(string='Subject ID')
    subject_code = fields.Char(string='Subject Code')
    subject_type= fields.Char(string='Subject Type')
    passing_marks = fields.Integer(string='Passing Marks')

    student_ids=fields.Many2many('res.partner','orm_subject_student_rel','subject_ids','student_ids',string='Students')

    @api.model_create_multi
    def create(self,vals):
        for val in vals:
            val['subject_type']='Practical'
        res = super(OrmSubject,self).create(vals)
        return res

    def write(self,vals):
        print(vals)
        if vals and vals.get('subject_id'):
            vals['subject_id']=vals['subject_id']+1
        res = super(OrmSubject,self).write(vals)
        return res