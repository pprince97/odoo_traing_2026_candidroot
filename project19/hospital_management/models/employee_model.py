from odoo import models,fields,api,Command

class Employee(models.Model):
    _inherit='hr.employee'

    is_medical_staff=fields.Boolean(string="Medical Staff")
    license_no=fields.Char("License Number")
    specialization=fields.Selection([('cardio','Cardio'),('neuro','Neuro'),('general','General')],"Specialization",default='general')
    consultation_fee=fields.Float("Consultation Fee")
    exp_years=fields.Integer("Experience Years")
    Joining_datetime=fields.Datetime("Joining Datetime")
    sign=fields.Image('Signature image')
    filename = fields.Char('Image Filename')
    notes=fields.Html('Notes')

    patient_ids=fields.One2many('patient.model','employee_id',string="Patients")

    @api.model_create_multi
    def create(self, vals):
        res = super(Employee, self).create(vals)
        for rec in res:
            rec.write({'patient_ids': [
                Command.create({'name':'command'}),
            ]})

            line=rec.env['patient.model'].search([('employee_id','=',rec.id)])
            rec.write({'patient_ids': [
                Command.update(line[0].id,{'age':'37'})
            ]})
        return res

    def write(self,vals):
        res = super(Employee, self).write(vals)

        if vals.get('exp_years'):
            line=self.env['patient.model'].search([('employee_id','=',self.id)])
            self.write({'patient_ids':[
                Command.delete(line.id)
            ]})

        if vals.get('notes'):
            line=self.env['patient.model'].search([('employee_id','=',self.id)])
            self.write({'patient_ids':[
                Command.unlink(line.id)
            ]})

        if vals.get('specialization'):
            self.write({'patient_ids': [Command.link(146)]})

        if vals.get('Joining_datetime'):
            self.write({'patient_ids':[Command.clear()]})

        if vals.get('consultation_fee'):
            line=self.env['patient.model'].search([('gender','=','male')])
            print(line.ids)
            self.write({'patient_ids':[Command.set(line.ids)]})
            print(self.patient_ids)
        return res


    def approve_doctor(self):
        doctor = self.env['doctor.model']
        return {
            'name': "Available Doctors",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'doctor.model',
            'target': 'self',
            'domain': [
                ("available", "=",1),
            ],
        }

    def open_patient_list(self):
        patient = self.env['patient.model']
        return {
            'name': "Patients",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'patient.model',
            'target': 'self',
            'domain': [
                ("doctor_emp_id", "=",self.id),
            ],
        }