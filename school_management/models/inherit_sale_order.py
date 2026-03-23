from odoo import models,fields, api
import math


class InheritSaleOrder(models.Model):
    _inherit = "sale.order"

    subject_id = fields.Integer(string="Subject ID")
    subject_code = fields.Char(string="Subject Code")
    subject_type = fields.Selection([('practical','Practical'),('theory','Theory')],string="Subject Type")
    subject_marks = fields.Float(string="Subject Marks")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['subject_type'] = 'theory'
        res = super(InheritSaleOrder,self).create(vals)
        return res
    #
    # def write(self, vals):
    #     vals['subject_marks'] = vals['subject_marks']+5
    #     res = super(InheritSaleOrder,self).write(vals)
    #     return res


