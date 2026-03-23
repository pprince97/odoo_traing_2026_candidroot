from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    barcode = fields.Char(string='Barcode')
    description = fields.Text(string='Description')
    book_currency = fields.Many2one('res.currency', string='Currency')
    state = fields.Selection([
        ('unpublished', 'Unpublished'),
        ('published', 'Published'),
    ],string='State',default='unpublished')
    category_id = fields.Many2one('book.category')
    available_copies = fields.Integer(string='Available Copies', tracking = True)
    stock = fields.Integer(string='Stock')
    cover_image = fields.Image(string='Cover Image')
    image_name = fields.Char(string='Image Name', tracking = True)
    borrow_price = fields.Float(string='Borrow Price')
    maximum_day_limit = fields.Integer(string='Maximum Day Limit', tracking = True)
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount')
    remaining_copies = fields.Char(string='Remaining Copies',compute='_compute_number_of_copies')
    borrow_lines_ids = fields.One2many('library.borrow.request.line','book_id',string='Borrow Lines')

    history_ids = fields.One2many('book.history','book_id',string='Book History')

    @api.depends('available_copies','stock')
    def _compute_number_of_copies(self):
        if self.stock and self.available_copies:
            self.remaining_copies =str(self.available_copies) +"/"+ str(self.stock)
        else:
            self.remaining_copies = ''


    def history_of_borrow_book(self):
        self.ensure_one()
        return {
            'name': "Book BorrowHistory",
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request.line',
            'view_mode': 'list,form',
            'target': 'Current',
            'domain': [('book_id', '=', self.id)],
        }


    @api.depends('fine_amount')
    def _compute_fine_amount(self):
        fine = self.env['ir.config_parameter'].sudo().get_param('library_management_man.fine_amount_value')
        for record in self:
            record.fine_amount = fine

    def published_book(self):
        self.update({
            'state': 'published',
        })

    def unpublished_book(self):
        self.update({
            'state': 'unpublished',
        })
        
    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            record['barcode'] = self.env['ir.sequence'].next_by_code('book.sequence')
        return super().create(vals)
