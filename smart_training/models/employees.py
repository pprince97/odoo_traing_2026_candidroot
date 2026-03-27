from odoo import models,fields,api

class Employees(models.Model):
    _inherit = "hr.employee"

    training_enrollment_ids =  fields.One2many('smart.training.enrollments','employee_id',string="Training Enrollments")
    certificate_ids = fields.One2many('smart.training.certificates','employee_id',string="Certificates")
    program_ids = fields.One2many('smart.training.programs','employee_id',string="Completed Program")
    total_trainings = fields.Integer(string="Total Trainings")
    total_certifications = fields.Integer(string="Total Certifications")
    training_score_avg =  fields.Float(string="Average Training Score")
    training_status =  fields.Selection([('not_started','Not Started'),('in_progress','In Progress'),('completed','Completed')],string="Training Status")
    mandatory_training_pending = fields.Boolean(string="Mandatory Training Pending")
    training_notes = fields.Text(string="Training Notes")
    skill_level= fields.Selection([('beginner','Beginner'),('intermediate','Intermediate'),('expert','Expert')],string="Skill Level")