from odoo import models, fields, api

class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'product.material'

    name = fields.Char(string="Material")
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    cost = fields.Monetary(string="Cost",currency_field='currency_id')

class ProductSurface(models.Model):
    _name = 'product.surface'
    _description = 'product.surface'

    name = fields.Char(string="Surface")
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    cost = fields.Monetary(currency_field='currency_id',string="Cost")

class ProductUvPrinting(models.Model):
    _name = 'product.uv.printing'
    _description = 'product.uv.printing'

    name = fields.Char(string="UV Printing")
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    cost = fields.Monetary(currency_field='currency_id',string="Cost")

class ProductColourShade(models.Model):
    _name = 'product.colour.shade'
    _description = 'product.colour.shade'

    name = fields.Char(string="Colour Shade")
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.ref('base.USD'), store=True
    )
    cost = fields.Monetary(currency_field='currency_id',string="Cost")