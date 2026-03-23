from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class BorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Library Borrow Request'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number')
    student_id = fields.Many2one('res.partner', string='Student',domain=[('student_code','ilike','S%')],required=True)
    librarian_id = fields.Many2one('res.partner', string='Librarian',domain=[('librarian_code','ilike','L%')],required=True)
    state = fields.Selection([('draft','Draft'),('issued','Issued'),('returned','Returned'),('cancelled','Cancelled')],string='State',default='draft')
    issue_date = fields.Date(string='Issue Date')
    return_date = fields.Date(string='Return Date')
    fine_amount = fields.Float(string='Fine Amount',compute='_compute_fine_amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount')
    cancelled_date = fields.Date(string='Cancelled Date',readonly=True)
    cancellation_reason = fields.Char(string='Cancellation Reason',readonly=True)
    borrow_request_ids = fields.One2many('library.borrow.request.lines','borrow_request_id',string='Borrow Request lines')

    fine_amount_config = fields.Float(string="Fine Amount Config",compute="_compute_fine_amount_config")


    def issued_books(self):
        self.state = 'issued'
        self.issue_date = fields.Date.today()
        for line in self.borrow_request_ids:
            if line.book_id.available_copies - line.quantity < 0 :
                raise ValidationError(_('Copies are not available'))
            else:
                line.book_id.available_copies -= line.quantity


    def returned_books(self):
        self.state = 'returned'
        self.return_date = fields.Date.today()
        for line in self.borrow_request_ids:
            line.book_id.available_copies += line.quantity
            if self.return_date > line.return_date:
                line.fine_amount = self.fine_amount_config*(self.return_date-line.return_date).days
            line.total_amount = line.amount*line.quantity + line.fine_amount

    def cancelled_books(self):
        return {
            'name': 'Cancel Borrow Request',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_serial_number': self.serial_number},
        }

    @api.model_create_multi
    def create(self, vals):
        res = super(BorrowRequest, self).create(vals)
        for rec in res:
            rec.serial_number = self.env['ir.sequence'].next_by_code('borrow.sequence') or 'New'
        return res

    @api.depends('borrow_request_ids')
    def _compute_total_amount(self):
        total = 0.0
        for task in self.borrow_request_ids:
            total+= task.total_amount
        self.total_amount = total

    @api.depends('borrow_request_ids')
    def _compute_fine_amount(self):
        total = 0.0
        for task in self.borrow_request_ids:
            total+= task.fine_amount
        self.fine_amount = total

    @api.onchange('issue_date')
    def _onchange_issue_date(self):
        for rec in self:
            if rec.issue_date and rec.return_date and rec.issue_date >rec.return_date:
                raise ValidationError(_('Issued date cannot be greater than Returned date'))

    @api.onchange('return_date')
    def _onchange_return_date(self):
        for rec in self:
            if  rec.issue_date and rec.return_date and rec.issue_date > rec.return_date:
                raise ValidationError(_('Returned date cannot be lesser than Issued date'))

    def _compute_fine_amount_config(self):
        show_amount = self.env['ir.config_parameter'].sudo().get_param('library_management.fine_amount_per_dayy')
        for rec in self:
            rec.fine_amount_config = show_amount

    @api.model
    def default_get(self,fields):
        defaults = super(BorrowRequest, self).default_get(fields)
        if 'librarian_id' in fields:
            defaults['librarian_id'] = self.env.user.partner_id.id
        return defaults
