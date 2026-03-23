from odoo import models,fields,api

class DepartmentWizard(models.TransientModel):
    _name = 'create.department.wizard'
    _description = 'Create department wizard'

    name = fields.Char(string="Name")

    def create_department_wizard(self):
        res =self.env['hospital.department'].create({'name': self.name})
        return res
