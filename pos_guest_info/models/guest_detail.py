
from odoo import fields, models , api


class GuestDetail(models.Model):
    _name = "guest.detail"
    _inherit = ['pos.load.mixin']
    _description = "Guest Detail"

    # no_of_male = fields.Integer(string="No. of Male")
    # no_of_female = fields.Integer(string="No. of Female")
    # no_of_guest = fields.Integer(string="No. of Guest" , compute="_compute_no_of_guest")

    age = fields.Integer(string="Age")
    country = fields.Char(string="County")
    gender = fields.Char(string="Gender")

    guest_count_id = fields.Many2one('guest.count', string="Guest Count ID")
    no_of_guest = fields.Integer(string="No of Guest")

    pos_order_id = fields.Many2one('pos.order', string="Pos Order")

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ["id", "age", "country", "gender","write_date"]