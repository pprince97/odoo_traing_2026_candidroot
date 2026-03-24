from odoo import fields, models, api
from odoo.exceptions import ValidationError
from pygments.lexer import default


class Books(models.Model):
    _name = 'library.books'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Books'

    student_id = fields.Many2one('res.partner',string='Student')

    name = fields.Char(required=True, tracking=True)
    # book_id = fields.Many2one(related='file.upload.history.book_id', string='Book')
    barcode = fields.Char(required=True)

    description = fields.Text(string='Description')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')

    state = fields.Selection([
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    ],
        string='Status',
    )

    category = fields.Selection([
        ('anime', 'Anime'),
        ('hollywood', 'Hollywood'),
        ('motivation', 'Motivation'),
        ('music', 'Music'),
        ('other', 'Other'),
    ])

    borrow_price = fields.Float(string='Borrow Price', required=True)
    maximum_day_limit = fields.Integer(string='Maximum Day Limit')


    borrow_ids = fields.Many2many('library.borrow.request', 'borrow_books_rel', 'borrow_id', 'books_id',
                                  string='Borrow')


    # Dynamic config value change
    fine_amount = fields.Float(string='Fine Amount', default=lambda self: (
        self.env['ir.config_parameter'].sudo().get_param('library_management.fines_amounts_book', 0.0)
    ))

    def _compute_fine_amount(self):
        param = self.env['ir.config_parameter'].sudo().get_param('library_management.fines_amounts_book')

        for rec in self:
            if rec.fine_amount:
                rec.fine_amount = rec.fine_amount
            else:
                rec.fine_amount = param

            print(rec.fine_amount)


    borrowed_count = fields.Integer(string='Borrowed Count', compute='get_all_books_data')

    def get_all_books_data(self):
        self.ensure_one()

        self.borrowed_count = self.env['borrow.request.line'].search_count([('book_id', '=', self.id)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Books Data',
            'res_model': 'borrow.request.line',
            'view_mode': 'list',
            'domain': [
                ('book_id', '=', self.id)
            ]
        }


    request_lines_ids = fields.One2many('borrow.request.line', 'book_id', string='Request_lines')
    available_copies = fields.Integer(string='Available Copies', compute='_compute_books_count')
    stock = fields.Integer(string='Stock')

    books_count = fields.Char(string='Books Count', compute='_compute_books_count')

    @api.depends('stock')
    def _compute_books_count(self):
        for rec in self:

            if not rec.available_copies or rec.available_copies == 0:
                rec.available_copies = rec.stock
                rec.books_count = f"{rec.available_copies} / {rec.stock}"


            count = 0
            for i in rec.request_lines_ids:
                if i.quantity:
                    count = rec.available_copies - i.quantity

                    store = 0

                    if i.borrow_request_id.state == 'issued':
                        rec.available_copies = count
                        store = count

                    if i.borrow_request_id.state == 'returned':
                        rec.available_copies += store
                        store = 0

            rec.books_count = f"{rec.available_copies} / {rec.stock}"


            # elif self.available_copies and self.stock and self.available_copies > self.stock:
            #     raise ValidationError('Available copies cannot be greater than stock')


    book_cover_name = fields.Char(string='Book Cover Name', tracking=True)
    cover_image = fields.Binary(string='Cover Image')

    history_ids = fields.One2many('file.upload.history', 'book_id', string="File History")



    @api.onchange('cover_image')
    def action_upload_file(self):

        res = self.env['file.upload.history'].create({
            'name': self.book_cover_name,
            'file': self.cover_image,
            'book_id': self._origin.id,
        })

        with open("/home/erp/Desktop/workspace/Project/Project_19/library_management/models/log.txt", "a+") as f:
            f.writelines(f"{self.book_cover_name, fields.Date.today(), self._origin.id}\n")

        print("============>", res)
