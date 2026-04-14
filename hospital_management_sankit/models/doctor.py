from odoo import fields , models , api


class Doctor(models.Model):
    _inherit = "res.partner"
    # _description = "Doctor"
    _rec_name = 'name'


    doctor_code = fields.Char(string="Doctor Code" , readonly=True)
    # name = fields.Char(string="Name" , required=True)
    address = fields.Char(string="Address")
    # phone = fields.Char(string="Phone")
    # email = fields.Char(string="Email")
    specialty_description = fields.Char(string="Specialty / Description")
    experience = fields.Char(string="Experience")

    department_id = fields.Many2one('hospital.department', string="Department")
    hospital_id = fields.Many2one('hospital.hospital', string="Hospital" )
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id' , string="Appointments")

    # def generate_doctor_code(self):
    #     print("compute patient code >>>>>>>>>>>")
    #     self.doctor_code = self.env['ir.sequence'].next_by_code('stock.orderpoint')

    def action_hospital_appointment_doctor(self):
        self.ensure_one()

        appointment = self.env['hospital.appointment'].search([('doctor_id', '=', self.id)])

        if len(appointment) == 1 or len(appointment) == 0:
            return {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.appointment',
                'domain': [('doctor_id', '=', self.id)],
                'view_mode': 'form',
                'res_id': appointment.id,
                'context': {
                    'default_doctor_id': self.id,
                }
            }
        else:
            return {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.appointment',
                'view_mode': 'list,form',
                'domain': [('doctor_id', '=', self.id)],
                'context': {
                    'default_doctor_id': self.id,
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if self.env.context.get('doctor'):
                val['doctor_code'] = self.env['ir.sequence'].next_by_code('doctor.seq') or 'New'
        res = super().create(vals_list)
        return res



