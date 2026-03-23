from odoo import models,fields,api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    subject_id = fields.Integer(string='Subject ID',required=True)
    subject_code = fields.Char(string='Subject Code',required=True)
    subject_type = fields.Selection([('type1','Type1'),('type2','Type2'),('type3','Type3')],'Subject Type',required=True)
    passing_marks = fields.Integer(string='Passing Marks',required=True)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['subject_id']='123'
        res = super(SaleOrderInherit, self).create(vals)
        return res

    def write(self, val):
        val['subject_code'] = '234'
        res = super(SaleOrderInherit, self).write(val)
        return res