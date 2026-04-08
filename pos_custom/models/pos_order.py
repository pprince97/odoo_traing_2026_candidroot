from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_selected = fields.Datetime('Table Join')
    table_left = fields.Datetime('Table Leave')

    total_no_of_guests = fields.Integer('Total No of Guests',compute='_compute_total_no_of_guests',store=True)
    no_of_male = fields.Integer('No of Male',store=True)
    no_of_female = fields.Integer('No of Female',store=True)

    # def _load_pos_data_fields(self, config):
    #     data = super()._load_pos_data_fields(config) or []
    #     return data + [
    #         'total_no_of_guests',
    #         'no_of_male',
    #         'no_of_female'
    #     ]

    def _compute_total_no_of_guests(self):
        for rec in self:
            rec.total_no_of_guests = (rec.no_of_male or 0) + (rec.no_of_female or 0)