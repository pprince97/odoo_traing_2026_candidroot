from email.policy import default

from odoo import models,fields,api,Command
from odoo.fields import Domain
from odoo.exceptions import ValidationError
from datetime import datetime

class Appointment(models.Model):
    _name='appointment.model'
    _description='Appointment'

    name=fields.Char(string='Name')

    patient_id=fields.Many2one('patient.model',string='Patient',ondelete='cascade')
    doctor_id=fields.Many2one('doctor.model',string='Doctor',ondelete='cascade')

    appointment_date=fields.Datetime(string='Appointment Date',readonly=True)
    status=fields.Selection([('draft','Draft'),('confirm','Confirm'),('done','Done'),('cancel','Cancel')],default='draft',string='Status')
    token_no=fields.Char(string='Token Number')
    fees=fields.Float(string='Fees',compute='_compute_fees',store=True)
    paid=fields.Boolean(string='Paid')
    description=fields.Text(string='Description',readonly=True)
    prescription=fields.Html(string='Prescription')
    attachment=fields.Binary(string='Attachment',attachment=True)
    file_name=fields.Char(string='File Name')
    followup_date=fields.Date(string='Followup Date')
    duration_mins=fields.Integer(string='Duration in Minutes')
    is_emergency=fields.Boolean(string='Is Emergency')

    partner_id=fields.Many2one('res.partner',string='Partner',ondelete='cascade')

    @api.onchange('partner_id','patient_id')
    def _onchange_partner_address(self):
        for rec in self:
            rec.description = rec.partner_id.medical_history
            rec.attachment=rec.patient_id.report_file
            print('\n\n >>>>>>>>>>>>>>', rec.description)

    @api.depends('status','partner_id')
    def _compute_fees(self):
        for rec in self:
            if rec.status in ['confirm','done'] and rec.fees==0:
                rec.fees = 500

    def _inverse_fees(self):
        for rec in self:
            rec.fees = rec.fees

    @api.model
    def _search_fees(self,operator,value):
        appointment_ids = self.env['appointment.model'].search_fetch([], ['fees'])
        appointment_ids = appointment_ids.filtered_domain([('fees', operator, value)])
        return [('id', 'in',appointment_ids.ids)]

    @api.model_create_multi
    def create(self, vals):
        res = super(Appointment, self).create(vals)
        for rec in res:
            if rec.partner_id:
                rec.partner_id.view_appointment()
        return res

    def write(self, vals):
        res = super(Appointment, self).write(vals)
        for rec in self:
            if rec.partner_id:
                rec.partner_id.view_appointment()
        return res

    def unlink(self):
        if self.status != 'cancel':
            raise ValidationError("You cannot unlink this appointment")
        else:
            res=super().unlink()
            return res


    def confirm_status(self):
        self.update({'status':'confirm','appointment_date':datetime.now()})
    def done_status(self):
        self.update({'status':'done'})
    def cancel_status(self):
        print("\n Cancelled field >>>>>> ", self.read())
        self.update({'status':'cancel','appointment_date':False})
        self.unlink()

    def change_description(self,records):
        for rec in records:
            if rec.token_no=='123':
                rec.update({'description':'Descr'})
