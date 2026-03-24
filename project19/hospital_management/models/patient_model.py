from odoo import models,fields,api
from odoo.fields import Domain

class Patient(models.Model):
    _name='patient.model'
    _inherits = {'res.partner': 'partner_id'}
    _description='Patient'

    name = fields.Char(related='partner_id.name', inherited=True, readonly=False,string='Name')
    partner_id=fields.Many2one('res.partner', string='Partner', required=True, ondelete='restrict')
    active_p=fields.Boolean('Active')
    age=fields.Integer('Age')
    dob=fields.Date('Date of Birth')
    gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
    address=fields.Text('Address')
    symptoms=fields.Text('Symptoms')
    priority=fields.Selection([('low','Low'),('normal','Normal'),('high','High')],'Priority')
    report_file=fields.Binary('Report File')
    report_name=fields.Char('Report Name',store=True)
    ref_field=fields.Selection([('partner','Partner'),('employee','Employee')],'Reference Field')

    employee_id=fields.Many2one('hr.employee',string='Employee')
    appointment_id=fields.One2many('appointment.model','patient_id',String='Appointments')

    doctor_id = fields.Many2one('doctor.model', 'Doctors',ondelete='cascade')
    doctor_emp_id=fields.Integer('Doctor Employee ID',related='doctor_id.employee_id.id',store=True)

    confirm_count=fields.Integer('Confirm Count')

    def admit_patient(self):
        self.active_p=True

    def discharge_patient(self):
        self.active_p=False

    def confirm_count_btn(self):
        appointment = self.env['appointment.model']
        self.confirm_count = appointment.search_count([
            ("status", "=", "confirm"),
            ("patient_id", "=", self.id),
        ])
        return {
            'name': "Confirmed Appointments",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'appointment.model',
            'target': 'self',
            'domain': [
                ("status", "=", "confirm"),
                ("patient_id", "=", self.id),
            ],
        }

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if self.env.context.get('test'):
            domain = Domain.OR([Domain('name', operator, name),
                                Domain('symptoms', operator, name)])
            records = self.search(domain)
            return [(record.id, record.display_name) for record in records]
        return super().name_search(name, domain, operator, limit)

    @api.model
    def name_create(self,name):
        appointment = self.create({'name':name,'active_p': True,'priority': 'normal'})
        print('............', appointment)
        return appointment.id, appointment.display_name
