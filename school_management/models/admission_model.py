from odoo import models,fields,api

class Admission(models.Model):
    _name='school.admission'
    _description='School Admission'
    _rec_name = 'stu_name'

    adm_date_time = fields.Datetime(string="Admission date time",default=fields.Datetime.now,readonly=True)
    stu_name = fields.Char(string="Student's full name")
    fa_gua_name = fields.Char(string="Father's or Guardian's full name")
    mother_name = fields.Char(string="Mother's full name")
    gender = fields.Selection([('male','male'),('female','female'),('other','other')],string="Gender")
    stu_dob = fields.Date(string="Student's date of birth")
    blood_group = fields.Char(string="Blood group")
    fa_gua_mo_no = fields.Char(string="Father's or Guardian's mobile no",)
    address = fields.Text(string="Address")
    standard = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
                                 ('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12')],
                                "Standard for admission", default='1')
    pre_school = fields.Char(string="Previous school Name")
    percentage = fields.Float(string="Last year percentage")
    stu_photo = fields.Image(string="Student Photo")
    school_id = fields.Many2one('school.school',ondelete='cascade',string="School")
    stage = fields.Selection([('new','New'),('inprogress','In Progress'),('confirm','Confirm')],string="Stage",default='new')


    @api.model_create_multi
    def create(self, vals):
        res = super(Admission,self).create(vals)
        for rec in res:
            rec.school_id.action_view_new_adm()
            rec.school_id.action_view_prog_adm()
            rec.school_id.action_view_con_adm()
        return res

    def write(self, vals):
        res = super(Admission, self).write(vals)
        for rec in self:
            rec.school_id.action_view_new_adm()
            rec.school_id.action_view_prog_adm()
            rec.school_id.action_view_con_adm()
        return res

    def inprogress_stage(self):
        self.write({'stage':'inprogress'})

    def confirm_stage(self):
        Student=self.env['school.student']
        Student.create({'name':self.stu_name,'gender':self.gender,'dob':self.stu_dob,'admission_date_time':self.adm_date_time,'photo':self.stu_photo,
                        'school_id':self.school_id.id})
        self.write({'stage': 'confirm'})

    def new_stage(self):
        self.write({'stage': 'new'})


    def admission_browse(self):
        record = self.env['school.school'].browse(self.school_id.id)
        print("browse :- school record",record)
