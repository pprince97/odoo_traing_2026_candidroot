from odoo import fields, models

class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"
    _description = "Mail Compose Message"

    def open_wizard(self):
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Sale Order',
        #     'res_model': 'sale.order',
        #     'view_mode': 'form',
        #     'target': 'new',  # IMPORTANT → opens as dialog
        # }

        return {'type': 'ir.actions.client', 'tag': 'owl_template.counter_action', 'target': 'new'}

    def action_open_attachment_dialog(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attachment Wizard',
            'res_model': 'attachment.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
