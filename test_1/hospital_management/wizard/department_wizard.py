from odoo import fields, models, api


class DepartmentWizard(models.TransientModel):
    _name = 'department.wizard'
    _description = 'Department Wizard'

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
    hospital_ids = fields.Many2many('hospital.model','hospital_department_wizard_relation','department_wizard_id','hospital_id',string='Hospital')

    def wizard_create(self):
        res = self.env['department.model'].create({'name': self.name})
        return res
