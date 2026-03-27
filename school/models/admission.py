from odoo import models,fields,api

class Admission(models.Model):
    _name = 'school.admission'
    _description = 'Admission'

    name = fields.Char(string='Students Name')
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    dob = fields.Date(string='Date of Birth')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email Address')
    blood_group = fields.Char(string='Blood Group')
    fees = fields.Float(string='Fees',readonly=True,default=25000)
    id_proof = fields.Binary(string='Student ID Proof')
    student_photo = fields.Image(string='Student Photo')

    stage = fields.Selection([('new','New'),
                              ('inprogress','In Progress'),
                              ('confirm','Confirm')],
                             default='new',string='Admission Stage')

    school_id = fields.Many2one('school.school',string='School Name')

    def in_progress_stage(self):
        self.update({'stage':'inprogress'})

    def confirm_stage(self):
        Student = self.env['school.students'].create({'name':self.name,
                        'gender':self.gender,
                        'school_id':self.school_id.id,
                        'is_active':True,
                        'admission_datetime':fields.Datetime.now()})
        self.update({'stage':'confirm'})

    def new_stage(self):
        self.update({'stage':'new'})

    # def admission_count(self):
    #     Admission = self.env['school.admission']
    #     self.new_count = Admission.search_count([('stage','=','new')])
    #     self.progress_count = Admission.search_count([('stage','=','inprogress')])
    #     self.confirm_count = Admission.search_count([('stage','=','confirm')])

        # print("\n ADMISSION COUNTS :  ")
        # print("NEW COUNTS :  ",self.new_count)
        # print("IN PROGRESS COUNTS :  ")
        # print("ADMISSION COUNTS :  ")

    @api.model_create_multi
    def create(self, vals):
        res = super(Admission, self).create(vals)
        for rec in res:
            if rec.school_id:
                rec.school_id.new_countt()
                rec.school_id.progress_countt()
                rec.school_id.confirm_countt()
        return res

    def write(self, vals):
        res = super(Admission, self).write(vals)
        for rec in self:
            if rec.school_id:
                rec.school_id.new_countt()
                rec.school_id.progress_countt()
                rec.school_id.confirm_countt()
        return res

    def get_admission_details(self):
        student = self.env['school.admission'].browse(self.id)

        print("\n\n\n -----------------------",student.read())
        print(self.id)
        print(self.ids)
        for i in self:
            print(i)
        if student.exists():
            print("\n\n\n\n ----------------------",student.name)
            return {
                'name': student.name,
            }
        else:
            return {'error': 'student not found'}
