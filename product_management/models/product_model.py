from odoo import fields,models,api

class Products(models.Model):
    _inherit = "product.product"

    multipart = fields.Boolean('Is Multipart product?')
    material_id = fields.Many2one('product.material',string='Material')
    color_id = fields.Many2one('product.color.shade',string='Color')
    surface_id = fields.Many2one('product.surface.finish',string='Surface')
    printing_id = fields.Many2one('product.uv.printing',string='Printing')
    product_cost = fields.Float(string='Product Cost',compute='_compute_product_cost',store=True)
    total_cost = fields.Float(string='Total Cost',compute='_compute_total_cost',store=True)
    accessories_cost = fields.Float(string='Accessories Cost',compute='_compute_accessories_cost',store=True)
    product_lines = fields.One2many('product.product.lines','product_id',string='Products')

    @api.depends('material_id','color_id','surface_id','printing_id','product_lines.total')
    def _compute_product_cost(self):
        for rec in self:
            rec.product_cost = 0
            if not rec.multipart:
                if rec.material_id:
                    rec.product_cost += rec.material_id.price
                if rec.color_id:
                    rec.product_cost += rec.color_id.price
                if rec.surface_id:
                    rec.product_cost += rec.surface_id.price
                if rec.printing_id:
                    rec.product_cost += rec.printing_id.price
            else:
                for acc in rec.product_lines:
                    if not acc.sub_product_id.categ_id or acc.sub_product_id.categ_id.id != (self.env.ref('product_management.product_category_accessories')).id:
                        rec.product_cost += acc.total


    @api.depends('product_lines.total')
    def _compute_accessories_cost(self):
        for rec in self:
            rec.accessories_cost = 0
            if not rec.multipart:
                for accessory in rec.product_lines:
                    rec.accessories_cost += accessory.total
            else:
                for acc in rec.product_lines:
                    if acc.sub_product_id.categ_id and acc.sub_product_id.categ_id.id == (self.env.ref('product_management.product_category_accessories')).id:
                        rec.accessories_cost += acc.total

    @api.depends('accessories_cost','product_cost','total_cost')
    def _compute_total_cost(self):
        for rec in self:
            if rec.categ_id and rec.categ_id.id == (self.env.ref('product_management.product_category_accessories')).id:
                rec.total_cost = rec.total_cost
            else:
                for product in rec:
                    product.total_cost = (product.accessories_cost + product.product_cost)





