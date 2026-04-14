from odoo import fields , models , api

class CreateAppointmentWizard(models.TransientModel):
    _name = 'wizard.create_appointment_wizard'

    hospital_id = fields.Many2one('hospital.hospital', string='Hospital')
    patient_id = fields.Many2one('res.partner', string='Patient')
    department_id = fields.Many2one('hospital.department', string='Department')
    doctor_id = fields.Many2one('res.partner',
                                string='Doctor',)

    def appointment_create(self):
        res = self.env['hospital.appointment'].create({
            'hospital_id': self.hospital_id.id,
            'patient_id': self.patient_id.id,
            'department_id': self.department_id.id,
            'doctor_id': self.doctor_id.id,
        })
        print("+++++RES",res)

    # @api.model
    # def default_get(self, fields_list):
    #     result = super().default_get(fields_list)
    #     # result['patient_id'] = self.env['res.partner'].search()
    #     print(result,"-----------")
    #
    #     #
    #     #
    #     #     # Set a static default value for 'field_one'
    #     # result['field_one'] = "Default Text"
    #
    #     return result
    #
    # # @api.model_create_multi
    # # def create(self, vals):
