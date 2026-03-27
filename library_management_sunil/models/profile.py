from odoo import models, fields, api
import base64
from odoo.exceptions import ValidationError


class WebsiteProfile(models.Model):
    _name = "website.profile"
    _description = "Website Profile"

    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string="State")
    city = fields.Char()
    address = fields.Text()
    zip_code = fields.Char()
    pdf_file = fields.Binary(string="PDF File")
    pdf_filename = fields.Char(string="File Name")

    @api.constrains('pdf_file')
    def _check_pdf_file(self):
        for rec in self:
            if rec.pdf_file:
                import base64
                import mimetypes
                content = base64.b64decode(rec.pdf_file)
                if len(content) > 10 * 1024 * 1024:
                    raise ValidationError("PDF file size cannot exceed 10 MB")
                if rec.pdf_filename:
                    mime_type, _ = mimetypes.guess_type(rec.pdf_filename)
                    if mime_type != 'application/pdf':
                        raise ValidationError("Only PDF files are allowed")
