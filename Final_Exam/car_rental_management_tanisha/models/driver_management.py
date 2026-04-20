from odoo import api, fields, models

class DriverManagement(models.Model):
    _inherit = 'res.partner'

    license_issue_date = fields.Date(string='License Issue Date')
    birth_date = fields.Date(string='Birth Date')
    is_handicap = fields.Boolean(string='Is Handicap')
    status = fields.Selection([('available','Available'),('on_going','On-Going')],string='Status')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Foreign Currency")
    per_day_rate = fields.Monetary(store=True, readonly=False, currency_field='currency_id', string='Per Day Rate')
    booking_count = fields.Integer(compute='_compute_booking_count')

    def _compute_booking_count(self):
        self.booking_count = self.env['rental.booking'].search_count([('vehicle_line_ids.driver_id', 'in', self.id)])

    def show_booking_history(self):
        dom = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'rental.booking',
            'view_mode': 'list,form',
            'domain': [('vehicle_line_ids.driver_id', 'in', self.id)],
            'target': 'self'
        }
        if self.booking_count == 1:
            dom['view_mode'] = 'form'
            dom['res_id'] = self.env['rental.booking'].search([('vehicle_line_ids.driver_id', 'in', self.id)]).id
        return dom