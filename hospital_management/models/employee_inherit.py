from odoo import models, fields, api


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    is_medical_staff = fields.Boolean(string='Is Medical Staff ?')
    license_no = fields.Char(string='License number', default="https://images.rawpixel.com/image_png_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvam9iNjgwLTE2Ni1wLWwxZGJ1cTN2LnBuZw.png")
    specialization = fields.Selection([('cardio', 'Cardio'), ('neuro', 'Neuro'), ('general', 'General')],
                                      string='Specialization', default='cardio')
    consult_fee = fields.Float(string='Consultation Fee', compute='compute_consult_fee', inverse='inverse_consult_fee',
                               store=True)
    exp_years = fields.Integer(string='Experience Years')
    joining_datetime = fields.Datetime(string='Joining Datetime')
    sign_img = fields.Image(string='Signature Image')
    notes_html = fields.Html(string='Notes')
    patient_ids = fields.Many2many('hospital.patient', 'patient_doctor_emp_rel', 'patient_id', 'doctor_emp_id',
                                   string='Patient IDs')


    @api.model_create_multi
    def create(self, vals_list):
        res = super(EmployeeInherit, self).create(vals_list)
        for rec in res:
            print("--------------------------",rec.patient_ids)
            rec.patient_ids.patient_list()
        return res

    # def write(self, vals_list):
    #     res = super(EmployeeInherit, self).write(vals_list)
    #     for rec in self:
    #         print("--------------------------",rec.patient_ids)
    #         # rec.patient_ids.patient_list()
    #     return res

    @api.depends('specialization')
    def compute_consult_fee(self):
        for rec in self:
            print("computeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            if rec.specialization == 'cardio':
                rec.consult_fee = 1000
            else:
                rec.consult_fee = 0

    def inverse_consult_fee(self):
        for rec in self:
            print("inverseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            if rec.consult_fee > 0:
                rec.consult_fee = 0
