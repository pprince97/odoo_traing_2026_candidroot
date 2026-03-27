from odoo import models, fields, api


class ProductInherit(models.Model):
    _inherit = 'product.product'

    is_multi_part = fields.Boolean(string='Multi-part')
    material_id = fields.Many2one('product.material', string='Material')
    surface_finishing_id = fields.Many2one('product.surface.finishing', string='Surface Finish')
    uv_printing_id = fields.Many2one('product.uv.printing', string='UV Printing')
    colour_shade_id = fields.Many2one('product.colour.shade', string='Colour')
    accessory_cost = fields.Float(string='Accessory Cost',compute='compute_costs')
    product_cost = fields.Float(string='Product Cost',compute='compute_costs')
    accessories_cost = fields.Float(string='Accessories Cost',)
    total_cost = fields.Float(string='Total Cost',compute='compute_costs')
    product_line_ids = fields.One2many('product.lines', 'part_product_id', string="Product Lines")

    @api.depends('is_multi_part', 'material_id', 'surface_finishing_id','uv_printing_id', 'colour_shade_id','product_line_ids')
    def compute_costs(self):
        for product in self:
            if product.categ_id == self.env.ref('products.product_category_name'):
                product.accessory_cost = product.accessories_cost
                product.product_cost =  product.accessories_cost
                product.total_cost =  product.accessories_cost
            else:
                if not product.is_multi_part:
                    a_cost = 0
                    p_cost = 0
                    if product.material_id:
                        p_cost += product.material_id.price
                    if product.surface_finishing_id:
                        p_cost += product.surface_finishing_id.price
                    if product.uv_printing_id:
                        p_cost += product.uv_printing_id.price
                    if product.colour_shade_id:
                        p_cost += product.colour_shade_id.price
                    product.product_cost = p_cost
                    for rec in product.product_line_ids:
                        rec.product_price = rec.product_id.accessories_cost
                        a_cost += rec.product_price * rec.product_quantity
                        rec.total_price = rec.product_price * rec.product_quantity
                    product.accessory_cost = a_cost
                    product.total_cost = a_cost + p_cost
                else:
                    a_cost = 0
                    p_cost = 0
                    for rec in product.product_line_ids:
                        if rec.product_id.categ_id == self.env.ref('products.product_category_name'):
                            rec.product_price = rec.product_id.accessories_cost
                            a_cost += rec.product_price * rec.product_quantity
                            rec.total_price = rec.product_price * rec.product_quantity
                        else:
                            rec.product_price = rec.product_id.total_cost
                            p_cost += rec.product_price * rec.product_quantity
                            rec.total_price = rec.product_price * rec.product_quantity
                    product.product_cost = p_cost
                    product.accessory_cost = a_cost
                    product.total_cost = a_cost + p_cost