from odoo import models,fields,api

class School(models.Model):
    _name='school.school'
    _description='School Model'

    name = fields.Char(string='School Name')
    address = fields.Char(string='School Address')

    student_ids = fields.One2many('school.student','school_id',string='Student IDs')
    class_ids = fields.Many2many('school.class','school_class_rel','school_id','class_id',string='Classes')
    teacher_ids = fields.One2many('school.teacher','school_id',string='Teachers')
    subject_ids = fields.Many2many('school.subject','school_subject_rel','school_id','subject_id',string='Subjects')
    active = fields.Boolean(string='Is Active',default=True)
    admission_ids = fields.One2many('school.admission','school_id',string='Admission')
    new_count = fields.Integer(string='New Count')
    in_progress_count = fields.Integer(string='New Count')
    confirm_count = fields.Integer(string='New Count')

    def new_state_count(self):
        self.new_count = self.env['school.admission'].search_count([('stage', '=', 'new'),('school_id', '=', self.id)])
        d= {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'form,list',
            'domain': [('stage', '=', 'new'), ('school_id', '=', self.id)],
            'target': self
        }
        if self.in_progress_count==1:
            d['view_mode'] = 'form'
            d['res_id'] = self.env['school.admission'].search(
                [('stage', '=', 'new'), ('school_id', '=', self.id)]).id
        return d


    def in_progress_state_count(self):
        self.in_progress_count = self.env['school.admission'].search_count([('stage', '=', 'in_progress'),('school_id', '=', self.id)])
        d= {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'view': [(False, 'list'), (False, 'form')],
            'domain': [('stage', '=', 'in_progress'), ('school_id', '=', self.id)],
            'target': self
        }
        if self.in_progress_count==1:
            d['view_mode'] = 'form'
            d['res_id'] = self.env['school.admission'].search(
                [('stage', '=', 'in_progress'), ('school_id', '=', self.id)]).id
        return d

    def confirm_state_count(self):
        self.confirm_count = self.env['school.admission'].search_count([('stage', '=', 'confirm'),('school_id', '=', self.id)])
        d= {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('stage', '=', 'confirm'), ('school_id', '=', self.id)],
            'target': self
        }
        if self.confirm_count == 1:
            d['view_mode'] = 'form'
            d['res_id'] = self.env['school.admission'].search([('stage', '=', 'confirm'),('school_id', '=', self.id)]).id
        return d

    @api.model
    def name_create(self,name):
        record = self.create({'name':name})
        print('created>>>>>>>>>>>>>>>>>>school name:',name)
        return record.id,record.display_name

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        result = super().name_search(name, domain=domain, operator=operator, limit=limit)
        print("name search>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if not result:
            print("No record found")
        return result