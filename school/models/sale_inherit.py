from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    subject_id = fields.Many2one('school.subjects',string="Subject ID")
    subject_code = fields.Integer(string="Subject Code")
    subject_type = fields.Selection([('practical','Practical'),('theory','Theory')],string="Subject Type")
    passing_marks = fields.Integer(string="Passing Marks")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['passing_marks'] = 35
        res = super(SaleOrder,self).create(vals)
        return res

    def write(self , vals):
        vals['subject_code'] = 1245
        res = super(SaleOrder,self).write(vals)
        return res
