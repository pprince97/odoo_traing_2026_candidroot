from odoo import models,fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details = fields.Boolean(related='pos_config_id.guest_details', readonly=False,config_parameter='owl_template.guest_details')
    timing = fields.Selection(related='pos_config_id.timing', readonly=False,config_parameter='owl_template.timing')
    details_required = fields.Boolean(related='pos_config_id.details_required', readonly=False,config_parameter='owl_template.details_required')


class PosConfig(models.Model):
    _inherit = 'pos.config'

    guest_details = fields.Boolean(string="Guest Details")
    timing = fields.Selection([('before', 'Order Before'), ('after', 'Order After')], string="Guest Details Timing",default='before')
    details_required = fields.Boolean(string="Guest Details Required")

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     params = super()._load_pos_data_fields(config_id)
    #     # print(>>>>>>>>>>>>>>>>>>>>>>>)
    #     # params += ['guest_details', 'timing', 'details_required']
    #     return params
