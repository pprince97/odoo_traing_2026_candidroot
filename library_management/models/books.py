from odoo import fields, models, api

class Books(models.Model):
    _name = 'library.books'
    _description = 'Books'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Book Name', required=True)
    barcode = fields.Char(string='Barcode')
    description = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency', string='Currency')
    state = fields.Selection([
        ('published', 'Published'),
        ('unpublished', 'Unpublished')
    ], string='State',tracking=True)
    category = fields.Selection([
        ('comedy', 'Comedy'),
        ('gk', 'G.K.'),
        ('novel', 'Novel'),
        ('tech', 'Tech'),
        ('fiction', 'Fiction')
    ], string="category")
    available_copies = fields.Integer(string='Available Copies', tracking=True,readonly=True)
    stock = fields.Integer(string='Stock',tracking=True, required=True)
    cover_image = fields.Image(string='Cover Image')
    borrow_price = fields.Float(string='Borrow Price(Per day)', required=True ,tracking=True)
    maximum_day_limit = fields.Integer(string='Maximum Day Limit',tracking=True)
    show_book = fields.Char()
    borrow_request_ids = fields.One2many('library.borrow.request', 'book_id')

    # ●​ Smart Button For Showing History of Borrowed (Only Librarian and Admin can see this Button)
    def show_history(self):
        pass

    # ●​ Smart Button For Showing Number of Counts Available Book (Not any action Needed)
    # ○​ Example : 06 / 10
    def show_available_copies(self):
        pass


    def book_reduce(self,book_id):
        for i in book_id:
            i.available_copies -= 1
            print(i.available_copies)
            i.show_book = str(self.available_copies) + ' / ' + str(self.stock)
            print(i.show_book)


    @api.onchange('available_copies','stock')
    def show_book_record(self):
        for doc in self:
            doc.show_book = str(self.available_copies) + ' / ' + str(self.stock)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('barcode'):
                vals['barcode'] = self.env['ir.sequence'].next_by_code('barcode.sequence')
        return super().create(vals_list)


# 1. Books
# Fields:
# Name (required)
# Barcode (required)
# Description
# Currency (res.currency)
# State (published/unpublished)
# Category
# Available Copies
# Stock
# Cover Image
# Borrow Price (per day) (required)
# Maximum Day Limit
# Business Rules:
# ●Demo Data For Create Books
# ●Admin and Librarians can create new Books and also Perform Operation of Publish and Unpublish Books.
# ●Librarians can see All Books and Its Stock, and can also change every detail of Books.
