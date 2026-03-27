from odoo import models,fields,api

class SmartTrainingEnrollments(models.Model):
    _name = "smart.training.enrollments"
    _description = "Smart Training Enrollments"

    employee_id = fields.Many2one('hr.employee',string="Employees")
    session_id = fields.Many2one('smart.training.sessions',string="Sessions")
    program_id = fields.Many2one('smart.training.programs',string="Programs")
    enrollment_date = fields.Date(string="Enrollment Date", default=fields.Date.today())
    attendance_percentage = fields.Float(string="Attendance Percentage")
    score = fields.Float(string="Score")
    result = fields.Selection([('pending', 'Pending'), ('passed', 'Passed'), ('failed', 'Failed')],
                                   string="Level",default='pending',required=True)
    certificate_id = fields.Many2one('smart.training.certificates',string="Certificate")
    feedback = fields.Text(string="Feedback")