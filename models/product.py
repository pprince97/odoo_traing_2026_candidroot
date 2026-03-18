from odoo import models, fields, api, Command

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_multipart = fields.Boolean(string="Is Multipart")
    type_selection = fields.Selection([
        ('product', 'Product'),
        ('subproduct', 'Subproduct'),
        ('accessory', 'Accessory'),
    ], string="Type", default='product')
    product_line_ids = fields.One2many('product.product.line',
                                       'product_id',
                                       string="Sub Products And Accessories")
    material_id = fields.Many2one('product.material', string="Material")
    surface_finish_id = fields.Many2one('product.surface', string="Surface Finishing")
    uv_printing_id = fields.Many2one('product.uv.printing', string="UV Printing")
    colour_shade_id = fields.Many2one('product.colour.shade', string="Colour Shade")
    cost = fields.Monetary(string="Cost", compute="_compute_cost", store=True, currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    accessories_cost = fields.Monetary(string="Accessories Cost",
                                       currency_field='currency_id',
                                    compute="_compute_accessories_cost", store=True)
    total_cost = fields.Monetary(string="Total Cost", currency_field='currency_id',
                              compute="_compute_total_cost", store=True)

    @api.depends(
        'product_line_ids',
        'type_selection',
        'standard_price'
    )
    def _compute_accessories_cost(self):
        for rec in self:
            if rec.type_selection == 'accessory':
                rec.accessories_cost = 0.0
            else:
                accessory = rec.product_line_ids.filtered(lambda l: l.product_selection_id.type_selection == 'accessory')
                rec.accessories_cost = sum(accessory.mapped('price'))

    @api.depends(
        'product_line_ids',
        'material_id',
        'surface_finish_id',
        'uv_printing_id',
        'colour_shade_id',
        'type_selection'
    )
    def _compute_cost(self):
        for rec in self:
            if rec.type_selection == 'accessory':
                rec.cost = 0.0
            else:
                subproducts = rec.product_line_ids.filtered(lambda l: l.product_id.type_selection != 'accessory')
                rec.cost = sum(subproducts.mapped('price')) + rec.material_id.cost + rec.surface_finish_id.cost + rec.uv_printing_id.cost + rec.colour_shade_id.cost

    @api.depends('cost', 'accessories_cost')
    def _compute_total_cost(self):
        for rec in self:
            if rec.type_selection == 'accessory':
                rec.total_cost = rec.standard_price
            else:
                rec.total_cost = rec.cost + rec.accessories_cost

class ProductProductLine(models.Model):
    _name = 'product.product.line'
    _description = 'product.product.line'

    product_id = fields.Many2one('product.product', string="Product")
    product_selection_id = fields.Many2one('product.product', string="Select Product", store=True,
                                 domain="[('id', 'in', allowed_product_ids)]")
    quantity = fields.Float(string="Quantity", default=1)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    unit_price_accessory = fields.Monetary(string="Price of Accessory", currency_field='currency_id',)
    price = fields.Monetary(string="Price", currency_field='currency_id',compute="_compute_price")

    allowed_product_ids = fields.Many2many(
        'product.product',
        compute='_compute_allowed_products'
    )

    @api.depends('product_selection_id', 'product_id.type_selection', 'product_id.is_multipart')
    def _compute_allowed_products(self):
        product = self.env['product.product']

        for rec in self:
            if rec.product_id.is_multipart:
                products = product.search([
                    ('type_selection', 'in', ['subproduct', 'accessory']),
                ])
            else:
                products = product.search([
                    ('type_selection', '=', 'accessory'),
                ])

            rec.allowed_product_ids = [Command.set(products.ids)]

    @api.depends('product_selection_id', 'quantity')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.quantity * (rec.product_selection_id.total_cost or 0.0)
