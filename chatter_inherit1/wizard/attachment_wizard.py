from odoo import models, fields

class AttachmentWizard(models.TransientModel):
    _name = 'attachment.wizard'

    file_ids = fields.Many2many('ir.attachment')

    def action_attach_files(self):
        composer_id = self.env.context.get('composer_id')

        composer = self.env['mail.compose.message'].browse(composer_id)

        composer.write({
            'attachment_ids': [(6, 0, self.file_ids.ids)]
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'res_id': composer_id,
            'target': 'new',
        }