from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Patients(models.Model):
    _inherit = 'res.partner'

    patient_code = fields.Char(string="Patient Code",readonly=True)
    date_of_birth = fields.Date(string="Date of Birth"  )
    age = fields.Char(string="Age",compute="_compute_age")
    age_years = fields.Integer(compute="_compute_age")
    hospital_id = fields.Many2one('hospital.management.hospitals',string='Hospitals')
    pat_appointment_ids = fields.One2many('hospital.management.appointments','patient_id',string='Appointments')
    appointment_count = fields.Integer(compute="_compute_appointment_count")
    prescription_ids = fields.One2many('hospital.management.prescriptions','patient_id',string='Prescriptions')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for patient in self:
            if patient.date_of_birth:
                age = relativedelta(fields.Date.today(),patient.date_of_birth)
                patient.age_years = relativedelta( fields.Date.today(),patient.date_of_birth).years
                patient.age = "Years: " + str(age.years) + " Months : " + str(age.months) + " Days: " + str(age.days)
            else:
                patient.age=0
                patient.age_years = 0


    @api.model_create_multi
    def create(self, vals_list):
        res = super(Patients, self).create(vals_list)
        for rec in res:
            if (self.env.context.get('new_patient') or self.env.context.get('patient')) and not rec.appointment_count:
                res.patient_code = self.env['ir.sequence'].next_by_code('patient.seq') or 'New'
                group_patient = self.env.ref('hospital_management_rushvi.group_hospital_patient')
                self.env['res.users'].create({
                    'name': rec.name,
                    'email': rec.email,
                    'login': rec.email,
                    'password': rec.email,
                    'group_ids': [(4, group_patient.id)],
                    'partner_id': rec.id
                })
        return res

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        if self.date_of_birth and self.date_of_birth > fields.Date.today():
            raise ValidationError("Birthdate Can't be in the future")

    @api.depends('pat_appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.management.appointments'].search_count([('patient_id', '=', rec.id)])

    def pat_view_appointments(self):
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.management.appointments',
            'view_mode': 'list,form',
            'domain': [('patient_id','=',self.id)],
            'context':{'default_patient_id':self.id},
            'target': 'current',
        }

    def appointment_create(self):
        return{
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.create.appointment.wizard',
            'view_mode': 'form',
            'target': 'new',
         }

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     patients = self.env['res.partner'].search_count([('category_id', '=', 'Patient')])
    #     tag = self.env['res.partner.category'].search([('name', '=', 'Patient')], limit=1)
    #     for rec in res:
    #         rec.patient_code = f"P{patients + 1:05d}"
    #         rec.category_id = [(5,0,0),(4,tag.id)]
    #     return res






















































