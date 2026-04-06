from odoo import models, fields

class AttachmentWizard(models.TransientModel):
    _name = 'attachment.wizard'
    _description = 'Attachment Wizard'

    name = fields.Char(string="Name")
    attachment = fields.Binary(string="Attachment")
    description = fields.Text(string="Description")