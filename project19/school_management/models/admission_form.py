from odoo import api,fields,models
from datetime import datetime

class AdmissionForm(models.Model):
    _name='admission.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Admission Form"

    name=fields.Char(string="Name",required=True,tracking=True)
    age=fields.Integer(string="Age")
    gender=fields.Selection([('male','Male'),('female','Female')],string="Gender",default='male')
    dob=fields.Date(string="Date of Birth")
    percentage=fields.Float(string="Percentage")
    std_for_admission = fields.Integer(string='Standard')
    previous_school=fields.Char(string="Previous School")
    address=fields.Text(string="Address")
    html=fields.Html(string="HTML")
    color=fields.Char(string="Color")
    k_color=fields.Char(string="KColor")
    is_active=fields.Boolean(string="Is Active")

    f_name=fields.Char(string="Father/Guardian Name")
    f_phone=fields.Char(string="Father/Guardian's Phone Number")
    f_email=fields.Char(string="Father/Guardian's Email")

    m_name=fields.Char(string="Mother Name")
    m_phone = fields.Integer(string="Mother's Phone Number")
    m_email = fields.Char(string="Mother's Email")

    s_photo=fields.Image(string="Student Photo")
    file_name_i=fields.Char(string="File Name")
    id_proof=fields.Binary(string="Student ID Proof")
    file_name=fields.Char(string="Image Name")
    bg_img=fields.Binary(string="Background Image")

    school_id=fields.Many2one('obj.school',string='School',ondelete='cascade')

    company_currency_id = fields.Many2one('res.currency')
    fees = fields.Float(string="Fees")
    state=fields.Selection(
        [('new','New'),
         ('in_progress','In Progress'),
         ('confirm','Confirm'),]
    ,string="State",default='new')

    @api.model_create_multi
    def create(self, vals):
        res = super(AdmissionForm, self).create(vals)
        for rec in res:
            if rec.school_id:
                rec.school_id.new_count_btn()
                rec.school_id.in_progress_count_btn()
                rec.school_id.confirm_count_btn()
        return res

    def write(self, vals):
        res = super(AdmissionForm, self).write(vals)
        for rec in self:
            if rec.school_id:
                rec.school_id.new_count_btn()
                rec.school_id.in_progress_count_btn()
                rec.school_id.confirm_count_btn()
        return res

    def new_state(self):
        self.update({'state':'new'})

    def in_progress_state(self):
        self.update({'state':'in_progress'})

    def confirm_state(self):
        self.update({'state':'confirm'})
        student=self.env['school.student'].search([])
        student.create({'name':self.name,'roll_number':1,'percentage':self.percentage,'gender':self.gender,'is_active':True,'dob':self.dob,'admission':datetime.now(),'id_proof':self.id_proof,'photo':self.s_photo,'school_id':self.school_id.id})

    def browse_btn(self):
        school = self.env['obj.school']
        bid = school.browse(self.school_id.id)
        print('.............', bid.name)

        school.update({'phone': self.m_phone})

    def name_create(self,name):
        partner = self.create({self.name:name})
        print("............",partner)
        return partner.id, partner.display_name

    def web_name_search(self, name, specification):
        id_name_pairs = self.name_search(name)
        records = self.browse([id for id, _ in id_name_pairs])
        print(id_name_pairs)
        return records.web_read(specification)

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id