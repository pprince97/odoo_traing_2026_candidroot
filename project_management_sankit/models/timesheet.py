from odoo import api, fields, models

class Timesheet(models.Model):
    _name = 'project.timesheet'
    _description = 'Timesheet'
    _rec_name = 'timesheet_code'


    timesheet_code = fields.Char(string='Timesheet Code' , readonly=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    description = fields.Text(string='Description')
    spend_hours = fields.Float(string='Spend hours' , readonly=True)

    tasks_id = fields.Many2one('project.tasks', string='Tasks')
    assignees_ids = fields.Many2many(related='tasks_id.task_assignees_ids')
    timesheet_assignees_ids = fields.Many2many('res.users', 'timesheet_assignees_user_rel', 'timesheet_user_id', 'timesheet_assignees_id',
                                          string='Assignees',
                                          domain="[('id', 'in', assignees_ids)]")
    project_id = fields.Many2one('project.projects', string='Project')
    hour_rate_ids = fields.One2many(related='project_id.rate_calculation_ids')

    price = fields.Float(string='Price')



    @api.onchange('start_date', 'end_date')
    def _onchange_start_end(self):
        if self.start_date and self.end_date and self.start_date <= self.end_date:
            spend_day = self.end_date - self.start_date
            self.spend_hours = spend_day.total_seconds() / 3600


    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['timesheet_code'] = self.env['ir.sequence'].next_by_code('timesheet.seq')
        res = super().create(vals_list)
        return res

    @api.onchange('tasks_id')
    def _onchange_tasks_id(self):
        self.project_id = self.tasks_id.project_id.id
        print(self.project_id.id,"===============")

    @api.onchange('spend_hours')
    def _onchange_spend_hours(self):
        self.price = 0.0
        for i in self.hour_rate_ids:
            if self.spend_hours >= i.to_hour:
                self.price += (i.to_hour - i.from_hour) * i.rate
                print(self.price)
                # self.spend_hours -= i.to_hour
            elif i.from_hour <= self.spend_hours <= i.to_hour:
                self.price += (self.spend_hours - i.from_hour ) * i.rate
                print(self.price)
            else:
                print(self.spend_hours,"---------")
                print(self.price,"---------")

