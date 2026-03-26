from odoo import models, fields,Command,api

class Teacher(models.Model):

    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name')
    emp_code = fields.Char(string='Employee Code')
    exp_years= fields.Integer(string='Experience years')
    salary = fields.Float(string='Salary')
    qualification = fields.Selection([('graduate','Graduate'),('post_graduate','Post graduate'),('phd','PHD')],string='Qualification',default='graduate')
    is_perm = fields.Boolean(string='Is Permanent?')
    joining_date= fields.Date(string='Joining date')
    last_login = fields.Datetime(string='Last Login')
    certificate = fields.Binary(string='Certificate')
    file_name1= fields.Char(string='File Name2')
    image = fields.Image(string='Image')
    file_name_i1= fields.Char(string='File Name3')

    student_ids=fields.Many2many('school.student','teacher_student_rel','teacher_id','student_id',string='Students')
    # subject_id=fields.Many2one('school.subject',string='Subject',ondelete='cascade')
    school_id2=fields.Many2one('obj.school',string='School',ondelete='cascade')

    @api.model_create_multi
    def create(self, vals):
        res = super(Teacher, self).create(vals)
        for rec in res:
            rec.write({'student_ids': [
                (0,0,{'name': 'command'}),
            ]})

            line = rec.env['school.student'].search([('teacher_ids','=',rec.id)])
            rec.write({'student_ids': [
                (1,line[0].id, {'roll_number': 37})
            ]})
        return res

    def write(self, vals):
        res = super(Teacher, self).write(vals)

        if vals.get('emp_code'):
            line = self.env['school.student'].search([('teacher_ids','=',self.id)])
            self.write({'student_ids': [
                (2,line.id,0)
            ]})

        if vals.get('exp_years'):
            line = self.env['school.student'].search([('teacher_ids','=',self.id)])
            self.write({'student_ids': [
                (3,line.id,0)
            ]})

        if vals.get('salary'):
            self.write({'student_ids': [(4,64,0)]})

        if vals.get('qualification'):
            self.write({'student_ids': [(5,0,0)]})

        if vals.get('joining_date'):
            line = self.env['school.student'].search([('roll_number','=',37)])
            print(line.ids)
            self.write({'student_ids': [(6,0,line.ids)]})
        return res