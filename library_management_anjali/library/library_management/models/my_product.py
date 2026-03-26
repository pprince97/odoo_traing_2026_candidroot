from odoo import models,fields,api,_

class MyProduct(models.Model):
    _name = "my.product"
    _description = "My Product"

    name = fields.Char(string="Name")