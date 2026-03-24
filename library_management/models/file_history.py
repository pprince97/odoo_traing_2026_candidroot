from odoo import models, fields, api

class FileUploadHistory(models.Model):
    _name = 'file.upload.history'
    _description = 'File Upload History'

    name = fields.Char("File Name")
    file = fields.Binary("File")
    upload_date = fields.Datetime(default=fields.Datetime.now)

    book_id = fields.Many2one('library.books', string="Related Record")

