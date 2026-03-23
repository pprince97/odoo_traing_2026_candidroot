from odoo import models,fields,api

class School(models.Model):
    _name = 'school.school'
    _description = 'School'

    name = fields.Char(string='Name')
    area = fields.Char(string='Area')
    student_ids=fields.One2many('school.student','school_id',string='Students')
    class_ids=fields.Many2many('school.class','school_class_rel','school_id','class_id',string='Classes')
    teacher_ids=fields.One2many('school.teacher','school_id',string='Teachers')
    subject_ids=fields.Many2many('school.subject','school_subject_rel','school_id','subject_id',string='Subjects')
    admission_ids = fields.One2many('school.admission','school_id',string='Admissions')
    new_count = fields.Integer(string="New Admission Count")
    pro_count = fields.Integer(string="Progress Count")
    con_count = fields.Integer(string="Confirm Count")



    def action_view_new_adm(self):
        self.new_count = self.env['school.admission'].search_count([('stage', '=', 'new'),('school_id', '=', self.id)])
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('stage', '=', 'new'), ('school_id', '=', self.id)],
        }

    def action_view_prog_adm(self):
        self.pro_count = self.env['school.admission'].search_count([('stage', '=', 'inprogress'),('school_id', '=', self.id)])
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('stage', '=', 'inprogress'), ('school_id', '=', self.id)],
        }

    def action_view_con_adm(self):
        self.con_count = self.env['school.admission'].search_count([('stage', '=', 'confirm'),('school_id', '=', self.id)])
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('stage', '=', 'confirm'), ('school_id', '=', self.id)],
        }

    @api.model
    def name_create(self, name):
        record = self.create({'name':name})
        print("school name ------------------------", name)
        print("name_create :- school record >>>>>>>>>>>>>",record)
        # print(record.id)
        # print(record.display_name)
        return record.id,record.display_name

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        record = super().name_search(name=name, domain=domain, operator=operator, limit=limit)
        print("name_search :- school record >>>>>>>>>>>>>>", record)
        return record


