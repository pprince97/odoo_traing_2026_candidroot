from odoo import models,fields,api,Command
from odoo.fields import Domain

class Doctor(models.Model):
    _name='doctor.model'
    _description='Doctor'
    _inherits={'hr.employee':'employee_id'}

    name=fields.Char(string='Name',related='employee_id.name', inherited=True, readonly=False)
    department=fields.Selection([('opd','Opd'),('surgery','Surgery'),('icu','ICU')],'Department')
    available=fields.Boolean('Available')
    room_no=fields.Char('Room Number')
    max_patients=fields.Integer('Max Patients')
    doc_img=fields.Image('Doctor Image')
    doc_img_name=fields.Char('Document Image Name')
    bio=fields.Text('Bio')
    date_start=fields.Datetime('Date Start')

    employee_id=fields.Many2one('hr.employee','Employee Id',ondelete='cascade', required=True)
    #
    # applicant_skill_ids = fields.One2many(
    #     "hr.applicant.skill", "applicant_id", string="Skills", copy=True
    # )
    # skill_ids = fields.Many2many("hr.skill", compute="_compute_skill_ids", store=True)

    def toggle_availability(self):
        self.available = not self.available

    # @api.depends("applicant_skill_ids.skill_id")
    # def _compute_skill_ids(self):
    #     for applicant in self:
    #         applicant.skill_ids = applicant.applicant_skill_ids.skill_id

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if self.env.context.get('test2'):
            domain = Domain.OR([Domain('name', operator, name), Domain('department', operator, name)])
            records = self.search(domain)
            return [(record.id, record.display_name) for record in records]
        return super().name_search(name, domain, operator, limit)


    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name'):
                self.env['hr.employee'].with_context(is_medical_staff=True)
        res = super().create(vals_list)
        return res