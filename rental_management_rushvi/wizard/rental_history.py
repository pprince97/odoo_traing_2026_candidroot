from odoo import models,fields,api

from odoo.exceptions import ValidationError


class RentalHistory(models.TransientModel):
    _name = 'wizard.rental.history'
    _description = 'Rental History'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    customer_ids = fields.Many2many('res.partner',string='Customer')

    def get_rental_history_records(self):
        return self.env['rental.order'].search([
            ('customer_id', 'in', self.customer_ids.ids),
            ('rent_end_date', '>=', self.start_date),
            ('rent_end_date', '<=', self.end_date),
        ])

    def generate_rental_history_report(self):
        return self.env.ref('rental_management_rushvi.rental_history_report').report_action(self)

    @api.onchange('start_date','end_date')
    def onchange_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date cannot be greater than end date')