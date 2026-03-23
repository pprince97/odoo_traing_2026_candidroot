from odoo import models, fields, api
from datetime import datetime


class Admission(models.Model):
    _name = 'school.admission'
    _description = 'Admission Model'

    student_name = fields.Char(string='Student Full Name')
    father_name = fields.Char(string='Father(Guardian) Full Name')
    mother_name = fields.Char(string='Mother Full Name')
    email = fields.Char(string='Email')
    phone = fields.Integer(string='Phone Number')
    dob = fields.Date(string='Date of Birth')
    percentage = fields.Float(string='Percentage')
    standard = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12')], string='Standard', default='1')
    address = fields.Text(string='Address')
    admission_date = fields.Datetime(string='Admission Date', default=datetime.now(), readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    id_proof = fields.Binary(string='ID proof', attachment=True)
    file_name = fields.Char(string='File Name')
    photo = fields.Image(string='Passport Photo')
    school_id = fields.Many2one('school.school', string='School', ondelete='cascade')
    stage = fields.Selection([('new', 'New'), ('in_progress', 'In_Progress'), ('confirm', 'Confirm')], string='Stage',
                             default='new')

    @api.model_create_multi
    def create(self, vals):
        res = super(Admission, self).create(vals)
        for rec in res:
            if rec.school_id:
                rec.school_id.new_state_count()
                rec.school_id.in_progress_state_count()
                rec.school_id.confirm_state_count()
        return res

    def write(self, vals):
        res = super(Admission, self).write(vals)
        for rec in self:
            if rec.school_id:
                rec.school_id.new_state_count()
                rec.school_id.in_progress_state_count()
                rec.school_id.confirm_state_count()
        return res

    def in_progress_state(self):
        self.write({'stage': "in_progress"})

    def confirm_state(self):
        Student = self.env['school.student']
        Student.create(
            {'name': self.student_name, 'email': self.email, 'percentage': self.percentage, 'gender': self.gender,
             'date_of_birth': self.dob,
             'admission_datetime': self.admission_date, 'id_proof': self.id_proof, 'file_name': self.file_name,
             'photo': self.photo, 'school_id': self.school_id.id})
        self.write({'stage': "confirm"})

    def new_state(self):
        self.write({'stage': "new"})

    def browse_state(self):
        rec = self.env['school.school'].browse(self.school_id.id)
        if rec:
            print("record found:",rec.name,rec.address)
        else:
            print("no record found")