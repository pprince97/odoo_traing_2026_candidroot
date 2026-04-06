from odoo import models, fields, api

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    attachment_ids = fields.Many2many(
        'ir.attachment',
        'attachment_mail_rel',
        'mail_id',
        'attachment_id',
        string='Attachments'
    )

    @api.model
    def get_record_attachments(self, model, res_id):
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', model),
            ('res_id', '=', res_id)
        ])
        return attachments.read(['id', 'name', 'mimetype'])

    def add_selected_attachments(self, attachment_ids):
        for wizard in self:
            wizard.attachment_ids = [(4, att_id) for att_id in attachment_ids]

    def attachment_button(self):
        return True