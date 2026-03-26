from odoo import api,fields,models,exceptions

class ProductLineModel(models.Model):
    _name = 'product.line'
    _description = 'Product Line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product',string="Product Id")
    quantity = fields.Integer(string="Quantity",default=1)
    sub_product_id = fields.Many2one('product.product',string="Products")

    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    cost = fields.Monetary('Total Cost Per Quantity', currency_field='company_currency_id')
    total_cost = fields.Monetary('Total Cost', currency_field='company_currency_id',compute='_compute_total_cost')

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id

    @api.depends('cost','quantity')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.cost * rec.quantity

    @api.onchange('sub_product_id')
    def _onchange_sub_product_id(self):
        for rec in self:
            if rec.sub_product_id:
                if rec.sub_product_id.categ_id.id == self.env.ref('product_management.accessory_demo').id:
                    rec.cost = rec.sub_product_id.standard_price
                else:
                    rec.cost = rec.sub_product_id.total_cost
            else:
                rec.cost = 0