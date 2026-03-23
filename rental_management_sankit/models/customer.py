from odoo import api, fields, models


class Customer(models.Model):
    _inherit = 'res.partner'


    rental_ids = fields.One2many('rental.order','customer_id',string='Rentals')


    def action_rental(self):
        self.ensure_one()
        return {
            'name': "Rental",
            'type': 'ir.actions.act_window',
            'res_model': 'rental.order',
            'domain': [('customer_id', '=', self.id)],
            'view_mode': 'list,form',
            'context': {
                'default_customer_id': self.id,
            }
        }


