# models/profile.py

from odoo import models, fields


class WebsiteProfile(models.Model):
    _name = "website.profile"
    _description = "Website Profile"

    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    country_id = fields.Many2one('res.country',string="Country")
    state_id = fields.Many2one('res.country.state', string="State")
    city = fields.Char()
    address = fields.Text()
    zip_code = fields.Char()
    pdf_file = fields.Binary(string="PDF file")

