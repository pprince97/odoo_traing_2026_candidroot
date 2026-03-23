from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class ReportWizard(models.TransientModel):
    _name = 'rental.report.wizard'
    _description = 'Rental Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)


    @api.onchange('start_date')
    def _onchange_start_date(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                rec.start_date = False
                raise ValidationError(_('start date must be less than end date'))

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.start_date > rec.end_date:
                rec.end_date = False
                raise ValidationError(_('end date must be grater than start date'))

    def wizard_rental_report(self):
        pass