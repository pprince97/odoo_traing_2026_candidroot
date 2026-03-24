from odoo import fields, models,api

class ProductVariant(models.Model):
    _inherit = 'product.product'

    multipart = fields.Boolean(string="Multipart")

    material_id = fields.Many2one('product.material',string="Material")
    surface_finish_id = fields.Many2one('product.surface.finish',string="Surface Finish")
    uv_printing_id = fields.Many2one('product.uv.printing',string="UV Printing")
    color_shade_id = fields.Many2one('product.color.shade',string="Color shade")

    product_line_ids = fields.One2many('product.line','product_id',string="Product Lines")

    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id',store=True)
    cost = fields.Monetary(string="Product Cost", currency_field='company_currency_id', compute='_compute_cost',store=True)
    accessories_cost = fields.Monetary('Accessories Cost', currency_field='company_currency_id', compute='_compute_accessories_cost',store=True)
    total_cost = fields.Monetary('Total Cost', currency_field='company_currency_id',compute='_compute_total_cost',store=True)

    @api.depends('material_id','surface_finish_id','uv_printing_id','color_shade_id','product_line_ids')
    def _compute_cost(self):
        for rec in self:
            if rec.material_id or rec.surface_finish_id or rec.uv_printing_id or rec.color_shade_id:
                rec.cost = rec.material_id.cost + rec.surface_finish_id.cost + rec.uv_printing_id.cost + rec.color_shade_id.cost
            else:
                if rec.product_line_ids:
                    rec.cost = 0
                    for line in rec.product_line_ids:
                        if line.sub_product_id.categ_id.id != self.env.ref('product_management.accessory_demo').id:
                            rec.cost += line.total_cost
                        else:
                            rec.cost = rec.cost
                else:
                    rec.cost = 0

    @api.depends('product_line_ids.total_cost')
    def _compute_accessories_cost(self):
        for rec in self:
            if rec.product_line_ids:
                rec.accessories_cost = 0
                for line in rec.product_line_ids:
                    if line.sub_product_id.categ_id.id == self.env.ref('product_management.accessory_demo').id:
                        rec.accessories_cost += line.total_cost
                    else:
                        rec.accessories_cost = rec.accessories_cost
            else:
                rec.accessories_cost = 0

    @api.depends('accessories_cost','cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.accessories_cost + rec.cost

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id