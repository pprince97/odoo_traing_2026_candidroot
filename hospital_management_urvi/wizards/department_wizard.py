from odoo import fields,models,api

class DepartmentWizard(models.TransientModel):
    _name = 'department.wizard'
    _description = 'Department Wizard'

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
    hospital_ids = fields.Many2many('hospital.hospital', 'hospital_department_wizard_rel', 'department_wizard_id', 'hospital_id',
                                    string='hospitals')

    @api.model
    def default_get(self, fields):
        # print(self.env.context['active_id'])
        defaults = super(DepartmentWizard,self).default_get(fields)
        print(defaults)
        if self.env.context.get('active_ids'):
            ids =self.env.context.get('active_ids')
            defaults['hospital_ids'] = self.env['hospital.hospital'].browse(ids)
            print(self.hospital_ids)
        # print(defaults)
        # print(self.hospital_ids)
        return defaults

    def wizard_create(self):
        res= self.env['hospital.department'].create({'name':self.name,'color':self.color})
        return res
