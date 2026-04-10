from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_selected = fields.Datetime('Table Join')
    table_left = fields.Datetime('Table Leave')

    total_no_of_guests = fields.Integer('Total No of Guests', store=True)
    no_of_male = fields.Integer('No of Male', store=True)
    no_of_female = fields.Integer('No of Female', store=True)
    guest_ids = fields.One2many('guest.details','order_id',string='Guest Details')