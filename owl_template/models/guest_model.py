from odoo import models, fields, api
import uuid

class Guest(models.Model):
    _name = 'pos.guest'
    _inherit = ['pos.load.mixin']
    _description = 'Guest'

    age = fields.Integer('Age')
    gender = fields.Selection([('male','male'),('female','female')],'Gender')
    country_id = fields.Many2one('res.country','Country')
    # uuid = fields.Char(string='UUID', readonly=True, index=True, default=lambda self: str(uuid.uuid4()))
    #
    # # The reference to the POS Order's UUID
    # pos_order_uuid = fields.Char(string='POS Order UUID', index=True)
    order_id = fields.Many2one('pos.order','Order')

    # @api.model
    # def _load_pos_data_fields(self,config):
    #     return [
    #         'id', 'age', 'gender', 'country_id', 'order_id','write_date'
    #     ]
    #
    # @api.model
    # def _load_pos_data_domain(self,config):
    #     return []

    # @api.model
    # def _load_pos_data_fields(self):
    #     return [
    #         'id', 'age', 'gender',
    #         'order_id', 'company_id', 'config_id',
    #         'session_id', 'user_id', 'country_id'
    #     ]

    # def _load_pos_data(self, data):
    #     domain = self._load_pos_data_domain()
    #     fields = self._load_pos_data_fields()
    #     return {
    #         'data': self.search_read(domain, fields, load=False),
    #         'fields': self._load_pos_data_fields(),
    #     }
