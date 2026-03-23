from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,_,Command


class Patient(models.Model):
    _inherit = "res.partner"

    patient_id = fields.Char(string="Patient ID",readonly=True)  #auto genrate
    # name = from res.partner
    date_of_birth = fields.Date(string="Date of Birth")
    age_ = fields.Char(string="Age",compute="_compute_age",store=True)
    # address = from res.partner
    # mobile= from res.partner
    # email= from res.partner
    # email= from res.partner
    member = fields.Selection([('doctor','Doctor'),('patient','Patient')],string="Member")
    hospital_ids_ = fields.Many2many('hospital.hospital', 'hospital_patient_rel', 'patient_id', 'hospital_id',
                                   string='Patients')
    pa_counts = fields.Integer(string="Appointment Count",compute="_compute_pa_count")

    def _compute_pa_count(self):
        self.pa_counts = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])

    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get("patient"):
            for val in vals:
                if val.get('patient_id','New') == 'New':
                    val['patient_id'] = self.env['ir.sequence'].next_by_code('patient.sequence') or 'New'
        res = super(Patient, self).create(vals)
        if self.env.context.get("patient"):
            for rec in res:
            #     if rec.member=='patient':
                    # p_id = self.env['res.partner'].search_count([('member', '=', 'patient')])
                    # if p_id < 10:
                    #     rec.patient_id = 'P000' + str(p_id)
                    # elif p_id < 100:
                    #     rec.patient_id = 'P00' + str(p_id)
                    # elif p_id < 1000:
                    #     rec.patient_id = 'P0' + str(p_id)
                    # else:
                    #     rec.patient_id = 'P' + str(p_id)
                    # print(rec.patient_id)
                    # if rec.patient_id == _('New'):
                    #     rec.patient_id = self.env['ir.sequence'].next_by_code('patient.seq') or _('New')
                if rec:
                    self.env['res.users'].create(
                        {'name': rec.name,
                         'email': rec.email,
                         'partner_id': rec.id,
                         'login': rec.name,
                         'password': rec.name,
                         'signature': rec.name,
                         'group_ids': [Command.set([self.env.ref('hospital_management_urvi.group_hospital_patient').id])]})
        return res


    def view_appointment_patient(self):
        rp = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': self
        }
        if self.pa_counts == 1:
            rp['view_mode'] = 'form'
            rp['res_id'] = self.env['hospital.appointment'].search(
                [('patient_id', '=', self.id)]).id
        return rp

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = fields.Date.today()
                delta = relativedelta(today, rec.date_of_birth)
                rec.age_ = f"{delta.years} Years, {delta.months} Months, {delta.days} Days"
            else:
                rec.age_ = False

