from odoo import api, fields, models

class TaskAssignees(models.Model):
    _inherit = 'res.users'

    available = fields.Boolean(string="Available" , default=True)
