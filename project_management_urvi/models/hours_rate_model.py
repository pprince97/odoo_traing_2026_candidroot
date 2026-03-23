from odoo import fields,models

class HoursRate(models.Model):
    _name = 'project.hours.rate'
    _description = 'Hours Rate Model'
    _rec_name = 'rate'

    s_hour = fields.Integer(string='Starting range of hours')
    e_hour = fields.Integer(string='Ending range of hours')
    currency_id = fields.Many2one('res.currency', string='Currency')
    rate = fields.Monetary(string='Rate',currency_field ='currency_id')
    system_para = fields.Boolean(string='System Para')

    def system_para_bool(self):
        print('>>>>>>>>>>>>',self.system_para)
        self.system_para = self.env['ir.config_parameter'].config.get_param('project_management_urvi.project_bill')
        print('>>>>>>>>>>>>',self.system_para)