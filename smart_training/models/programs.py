from odoo import models,fields,api

class SmartTrainingPrograms(models.Model):
    _name = "smart.training.programs"
    _description = "Smart Training Programs"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code",readonly=True)
    description = fields.Text(string="Description")
    category = fields.Selection([('technical','Technical'),('soft_skills','Soft Skills'),('management','Management')],
                                string="Category",required=True,default='technical')
    duration_hours = fields.Float(string="Duration Hours")
    level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')],
                                   string="Level",default='beginner',required=True)
    certification_available = fields.Boolean(string="Certification Available")
    passing_score = fields.Float(string="Passing Score")
    active = fields.Boolean(string="Active",default=True)
    trainer_ids = fields.Many2many('res.partner','trainer_program_rel','program_id','trainer_id',string="Trainers",domain=[('is_trainer','=',True)])
    session_ids = fields.One2many('smart.training.sessions','program_id',string="Sessions")
    employee_id = fields.Many2one('hr.employee',string="Employee")
    currency_id = fields.Many2one('res.currency',string='Currency')
    # , default = lambda self: self.env.company.currency_id  ,required=True
    fees = fields.Monetary(string="Fees",currency_field="currency_id")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SmartTrainingPrograms, self).create(vals_list)
        for rec in res:
            rec.code = f"PRG - {rec.id:05d}"
        return res

    @api.model
    def name_create(self, name):
        record_id, display_name = super().name_create(name)
        record = self.browse(record_id)
        record.certification_available = True
        return record_id, display_name