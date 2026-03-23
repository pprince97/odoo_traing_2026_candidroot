from odoo import models,fields,api

class ProductVariant(models.Model):
    _inherit = 'product.product'

    multi_parts = fields.Boolean(string='Multi parts? ')
    material_id = fields.Many2one(comodel_name='product.material',string='Material')
    surface_finishing_id = fields.Many2one(comodel_name='product.surface.finishing',string='Surface Finishing')
    uv_printing_id = fields.Many2one(comodel_name='product.uvprinting',string='UV Printing')
    color_shade_id = fields.Many2one(comodel_name='product.color.shade',string='Color Shade')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    product_cost = fields.Monetary(store=True, currency_field='currency_id', string='Product Cost', compute='_compute_product_cost')
    accessories_cost = fields.Monetary(store=True, currency_field='currency_id', string='Accessories Cost', compute='_compute_accessories_cost')
    total_cost = fields.Monetary(store=True, currency_field='currency_id', string='Total Cost', compute='_compute_total_cost')
    product_line_ids = fields.One2many(comodel_name='product.variant.lines',inverse_name='product_id')

    @api.depends('material_id','surface_finishing_id','uv_printing_id','color_shade_id','product_line_ids.total')
    def _compute_product_cost(self):
        for rec in self:
            if not rec.multi_parts and rec.categ_id != self.env.ref('product_management.product_category_accessory'):
                rec.product_cost = rec.material_id.cost + rec.surface_finishing_id.cost + rec.uv_printing_id.cost + rec.color_shade_id.cost
            elif rec.multi_parts and rec.categ_id != self.env.ref('product_management.product_category_accessory'):
                rec.product_cost = 0
                for product in self.product_line_ids:
                    if product.sub_product_id.categ_id != self.env.ref('product_management.product_category_accessory'):
                        rec.product_cost += product.total

    @api.depends('product_line_ids.total')
    def _compute_accessories_cost(self):
        for rec in self:
            if not rec.multi_parts and rec.categ_id != self.env.ref('product_management.product_category_accessory'):
                rec.accessories_cost = sum(rec.product_line_ids.mapped('total'))
            elif rec.multi_parts and rec.categ_id != self.env.ref('product_management.product_category_accessory'):
                rec.accessories_cost = 0
                for product in self.product_line_ids:
                    if product.sub_product_id.categ_id == self.env.ref('product_management.product_category_accessory'):
                        rec.accessories_cost += product.total

    @api.depends('product_cost','accessories_cost')
    def _compute_total_cost(self):
        for rec in self:
            if rec.categ_id != self.env.ref('product_management.product_category_accessory'):
                rec.total_cost = rec.product_cost + rec.accessories_cost

