from odoo import fields , api , models
from odoo.exceptions import ValidationError

class RateCalculation(models.Model):
    _name = 'project.rate_calculation'
    _description = 'Project Rate Calculation'

    from_hour = fields.Integer(string='From Hour')
    to_hour = fields.Integer(string='To Hour')
    rate = fields.Integer(string='Rate')
    # amount = fields.Float(string='Amount')


    projects_id = fields.Many2one('project.projects', string='Project')

    # @api.onchange('from_hour', 'to_hour', 'rate')
    # def _onchange_rate(self):
    #     if self.from_hour <= self.to_hour:
    #         self.amount =  (self.to_hour - self.from_hour) * self.rate
    #     else:
    #         raise ValidationError('From Hour must be lesser than To Hour')
