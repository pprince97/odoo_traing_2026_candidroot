from odoo import models,fields,api

class Subjects(models.Model):
	_name = 'school.subjects'
	_description = 'Subjects'

	name = fields.Char(string='Name')
	subject_code = fields.Char(string='Subject Code')
	max_marks = fields.Float(string='Max Marks')
	passing_marks = fields.Float(string='Passing Marks')
	subject_type = fields.Selection([('theory', 'Theory'),('practical','Practical')],string='Subject Type')
	is_optional = fields.Boolean(string='Is Optional')
	# active = fields.Boolean(string='Active')
	syllabus = fields.Text(string='Syllabus')
	reference_material = fields.Binary(string='Reference Material')
	icon= fields.Image(string='Icon')

	student_ids=fields.Many2many('school.students','student_subject_rel','subject_id','student_id',string='Students')
	school_ids = fields.Many2many('school.school','school_subject_rel','subject_id','school_id',string='Subjects')
	teacher_id = fields.One2many('school.teachers','subject_id','Teachers')

	res_partner_id= fields.Many2one('res.partner',string='Res Partner')