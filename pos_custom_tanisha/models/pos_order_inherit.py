from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_date_time = fields.Datetime()
    end_date_time = fields.Datetime()

    no_of_male = fields.Integer(string="No of Male")
    no_of_female = fields.Integer(string="No of Female")
    no_of_guest = fields.Integer(string="No of Guest")
    guest_ids = fields.One2many(comodel_name='guest.details', inverse_name='order_id', string='Guest Details')



class PosConfig(models.Model):
    _inherit = 'pos.config'

    guest_details_bool = fields.Boolean("Guest Details")
    guest_details_timing = fields.Selection([('order_before','Order Before'),('order_after','Order After')],string="Guest Details Timing", default='order_before')
    guest_details_req_bool = fields.Boolean("Guest Details Required")


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config):
        data = super()._load_pos_data_models(config)
        data += ['guest.details']
        return data
