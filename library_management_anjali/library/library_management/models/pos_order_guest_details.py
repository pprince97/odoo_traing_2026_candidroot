from odoo import fields, models, api

class PosOrderGuestDetails(models.Model):
   _name = "pos.order.guest.details"
   _description = "Pos Order Guest Details"

   order_id = fields.Many2one('pos.order',string="Order")
   age = fields.Integer(string="Age")
   nationality_id = fields.Many2one('res.country', string="Nationality")
   gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string="Gender")

