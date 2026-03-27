from odoo import models,fields,api

class SmartTrainingSessions(models.Model):
    _name = "smart.training.sessions"
    _description = "Smart Training Sessions"

    name = fields.Char(string="Name")
    program_id = fields.Many2one('smart.training.programs',string="Program")
    trainer_id = fields.Many2one('res.partner',string="Trainer",domain=[('is_trainer','=',True)])
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    location = fields.Char(string="Location")
    level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')],
                                   string="Level",default='beginner',required=True)
    capacity = fields.Integer(string="Capacity")
    # enrolled_count = fields.Float(string="Passing Score") - compute
    state = fields.Selection([('draft','Draft'),('scheduled','Scheduled'),('ongoing','Ongoing'),('completed','Completed'),('cancelled','Cancelled')]
                             ,string="State",default='draft')
    enrollment_ids = fields.One2many('smart.training.enrollments','session_id',string="Sessions")

    def scheduled_state(self):
        self.state = 'scheduled'

    def ongoing_state(self):
        self.state = 'ongoing'

    def completed_state(self):
        self.state = 'completed'

    def cancelled_state(self):
        self.state = 'cancelled'

    def action_draft_state(self):
        self.state = 'draft'