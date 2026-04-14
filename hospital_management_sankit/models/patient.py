import datetime


from odoo import fields , api , models
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _inherit = "res.partner"
    _rec_name = 'name'


    patient_code = fields.Char(string="Patient Code", readonly=True)
    # name = fields.Char(string="Name" , required=True)
    dob = fields.Datetime(string="Date of Birth")
    age_year = fields.Integer(string="Age Year",compute="_compute_age" , inverse='_inverse_age' ,readonly=True , store=True)
    age_month = fields.Integer(string="Age Month",readonly=True)
    age_day = fields.Integer(string="Age Day" ,readonly=True)
    # address = fields.Char(string="Address")
    # phone = fields.Char(string="Phone")
    # email = fields.Char(string="Email")

    p_hospital_id = fields.Many2one('hospital.hospital', string="Hospital" )
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    patient_count = fields.Integer(compute="_compute_patient_count", string="Patients")




    # def generate_patient_code(self):
    #     print("compute patient code >>>>>>>>>>>")
    #     self.patient_code = self.env['ir.sequence'].next_by_code('patient.seq')

    @api.depends('dob')
    def _compute_age(self):
        date_today = datetime.date.today()
        for rec in self:
            if rec.dob:
                rec.age_year = date_today.year - rec.dob.year
                rec.age_month = date_today.month - rec.dob.month
                if rec.age_month < 0 :
                    rec.age_year = rec.age_year - 1
                    rec.age_month = rec.age_month + 12
                rec.age_day = date_today.day - rec.dob.day
                if rec.age_day < 0 :
                    rec.age_day = rec.age_day + 30
                print("age", rec.age_year)
            else:
                rec.age_year = 0



    # def _inverse_age(self):
    #     date_today = datetime.date.today().year
    #     for rec in self:
    #         if rec.age_year:
    #             print(rec.age_year)
    #             rec.dob = datetime.date(date_today - rec.age_, rec.dob.month, rec.dob.day)
    #             print("dob", rec.dob)
    #         else:
    #             rec.dob = 0


    # def create(self, vals):
    #     self.patient_code = self.env['ir.sequence'].next_by_code('mrp.unbuild')
    #     res = super().create(vals)
    #     return res
    def _compute_patient_count(self):
        self.patient_count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])

    def action_hospital_appointment_patient(self):
        self.ensure_one()

        appointment = self.env['hospital.appointment'].search([('patient_id', '=', self.id)])

        if len(appointment) == 1 :
            return {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.appointment',
                'domain': [('patient_id', '=', self.id)],
                'view_mode': 'form',
                'res_id': appointment.id,
                'context': {
                    'default_patient_id': self.id,
                }

            }
        else:
            return {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.appointment',
                'view_mode': 'list,form',
                'domain': [('patient_id', '=', self.id)],
                'context': {
                    'default_patient_id': self.id,
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if self.env.context.get('patient'):
                val['patient_code'] = self.env['ir.sequence'].next_by_code('patient.seq') or 'New'
        res = super().create(vals_list)
        return  res


    def create_appointment(self):

        return {
            'name': "Appointment",
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.create_appointment_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }

        }
