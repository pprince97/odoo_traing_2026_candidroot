from odoo import models,fields,api

class Employees(models.Model):
    _inherit = "res.partner"

    is_trainer = fields.Boolean(string="Is Trainer",default=False)
    trainer_code = fields.Char(string="Training Code")
    specialization = fields.Char(string="Specialization")
    # session_ids =fields.Many2one('smart.training.sessions','trainer_id',string="Sessions")
    # total_sessions = compute
    # total_trainees = compute
    certification_level = fields.Selection([('internal','Internal'),('external','External')],
                                           default='internal',required=True,string="Certification Level")
    contract_type = fields.Selection([('internal','Internal'),('external','External'),('consultant','Consultant')],
                                     string="Contract Type",default='internal',required=True)
    availability_status = fields.Selection([('available','Available'),('busy','Busy'),('on_leave','On Leave')],
                                           default='available',required=True,string="Availability Status")
    trainer_notes = fields.Text(string="Training Notes")
    program_ids = fields.Many2many('smart.training.programs','trainer_program_rel','trainer_id','program_id',string="Programs")