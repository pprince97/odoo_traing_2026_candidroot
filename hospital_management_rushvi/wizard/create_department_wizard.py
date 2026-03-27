from odoo import models,fields,api

class CreateAppointmentWizard(models.TransientModel):
    _name = 'wizard.create.department.wizard'
    _description = 'Create Department Wizard'

    name = fields.Char(string='Name', required=True)
    dept_code = fields.Char(string='Dept Code')

    def create_department(self):
        return self.env['hospital.management.departments'].create({
            'name': self.name,
            'dept_code': self.dept_code
        })