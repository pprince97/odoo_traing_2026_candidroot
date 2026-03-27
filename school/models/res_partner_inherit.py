from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_id = fields.Many2one('school.students', string='Student ID')
    student_address = fields.Char(string='Student Address')
    student_roll_no = fields.Integer(string='Student Roll No')
    student_dob = fields.Date(string='Student DOB')
    subject_ids = fields.One2many('school.subjects','res_partner_id',string='Subjects')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['student_address'] = "Hostel"
        res = super(ResPartner,self).create(vals_list)
        return res

    def write(self,vals):
        if vals and vals.get('student_roll_no'):
            vals['student_roll_no']=12
        res = super(ResPartner, self).write(vals)
        # print("\n\nlllllllllllllllll",vals)
        return res