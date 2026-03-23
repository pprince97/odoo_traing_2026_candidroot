from odoo import models,fields,api,_,Command
from odoo.fields import Domain
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class InheritPatient(models.Model):
    _inherit = 'res.partner'

    patient_id = fields.Char(string='Patient ID')
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_compute_age')
    # pid = fields.Integer(default=1)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    hospital_ids = fields.Many2many('res.partner', 'hospital_patient_rel', 'patient_id', 'hospital_id',
                                    string='Hospitals')
    appointment_count = fields.Integer(compute='_compute_appointment_count')


    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get('patient'):
            vals[0]['patient_id'] = self.env['ir.sequence'].next_by_code('patient.seq') or 'New'
        res = super(InheritPatient, self).create(vals)
        # pid_rev=str(self.pid)[::-1]
        # print("---------------------------------", type(pid_rev),pid_rev)
        # while len(pid_rev)<4:
        #     pid_rev+='0'
        #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",pid_rev,len(pid_rev))
        # pid_rev='P'+pid_rev[::-1]
        # self.pid+=1
        # print("---------------------------------", pid_rev)
        # for rec in res:
        #     rec.write({
        #         'patient_id': pid_rev,
        #     })
        for rec in res:
            self.env['res.users'].create({
                'partner_id': rec.id,
                'name': rec.name,
                'email': rec.email,
                'phone': rec.phone,
                'login': rec.name,
                'password': rec.name,
                'group_ids': [Command.set([self.env.ref('hospital_management_tanisha.group_hospital_doctor').id])],
            })
        return res

    def _compute_appointment_count(self):
        self.appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])

    def patient_appointments(self):
        dom = {
            'name':self.name,
            'type':'ir.actions.act_window',
            'res_model':'hospital.appointment',
            'view_mode':'list,form',
            'domain':[('patient_id','=',self.id)],
            'context': {'default_patient_id':self.id},
            'target':'self'
        }
        if self.appointment_count==1:
            dom['view_mode']='form'
            dom['res_id'] = self.env['hospital.appointment'].search([('patient_id','=',self.id)]).id
        return dom

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Enter a valid date!!"))
            else:
                current_date = fields.Date.today()
                delta = relativedelta(current_date,rec.dob)
                rec.age=f"{delta.years} years {delta.months} months {delta.days} days"

    def create_appointment(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'create.appointment.wizard',
            'view_mode':'form',
            'target':'new',
        }
