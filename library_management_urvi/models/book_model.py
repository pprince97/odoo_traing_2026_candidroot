from odoo import models,fields,api,_,Command

from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string="Name",required=True)
    barcode = fields.Char(string="Barcode",required=True)
    description = fields.Text(string="Description",required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([('unpublished','Unpublished'),('published','Published')],string="State",default='unpublished')
    category = fields.Selection([('mystery','Mystery'),('horror','Horror'),('romantic','Romantic'),('science','Science'),('history','History'),('biography','Biography')],string="Category",default='mystery')
    available = fields.Integer(string="Available",compute='_compute_available')
    copies = fields.Integer(string="Copies")
    image = fields.Image(string="Image")
    borrow_price = fields.Monetary(string="Borrow Price",currency_field='currency_id',help="Enter price per day for the book",required=True)
    maximum_day_limit = fields.Integer(string="Maximum Day Limit")
    borrow_request_lines_ids = fields.One2many('library.borrow.request.line', 'book_id',
                                               string="Borrow Request Lines")
    borrow_book_history_count = fields.Integer(string="Borrow Book History",compute='_compute_borrow_book_history')
    image_history_ids = fields.One2many('library.image.history', 'book_id',string="Image History",compute='_compute_image_history')

    # to count available copies of particular book
    def _compute_available(self):
        for rec in self:
            if rec:
                not_available = self.env['library.borrow.request.line'].search([('book_id','=',rec.id),('borrow_request_id.state','=','issued')])
                not_available_count = 0
                for i in not_available:
                    if i.quantity:
                        not_available_count += i.quantity
                rec.available = rec.copies - not_available_count

    def _compute_borrow_book_history(self):
        self.borrow_book_history_count = self.env['library.borrow.request.line'].search_count([('book_id','=',self.id)])

    def borrow_book_history(self):
        a = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow.request.line',
            'view_mode': 'list,form',
            'domain': [('book_id','=',self.id)],
            'context': {'list_view_ref': 'borrow_request_lines_list_view'},
            'target': 'self'
        }
        if self.borrow_book_history_count == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['library.borrow.request.line'].search(
                [('book_id','=',self.id)])).id
        return a

    @api.onchange('barcode')
    def _onchange_barcode(self):
        for rec in self:
            if rec.barcode and self.env['library.book'].search_count([('barcode','=',rec.barcode)])>0:
                rec.barcode = False
                raise ValidationError(_("Barcode must be unique"))

    @api.onchange('image')
    def _compute_image_history(self):
        for rec in self:
            if rec.image:
                his = self.env['library.image.history'].create({'book_id':rec.id,'history_image':rec.image})
                self.write({
                    'image_history_ids': Command.link(his.id),
                            })
            else:
                rec.image_history_ids = rec.image_history_ids

    @api.model_create_multi
    def create(self,vals):
        self._onchange_barcode()
        rec = super(Book,self).create(vals)
        return rec

    def write(self, vals):
        res = super(Book, self).write(vals)
        for rec in self:
            if rec.image:
                self.env['library.image.history'].create({'book_id': rec['id']})
        return res