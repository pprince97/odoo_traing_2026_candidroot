from odoo import models, fields, api,_

from odoo.exceptions import ValidationError


class BorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow Request Model'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string="Serial Number", readonly=True, store=True)
    student_id = fields.Many2one(comodel_name='res.partner', string="Student", required=True)
    librarian_id = fields.Many2one(comodel_name='res.partner', string="Librarian", compute='_compute_librarian_id',
                                   store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('issued', 'Issued'), ('returned', 'Returned'), ('canceled', 'Canceled')], string="State",
        default='draft')
    issued_date = fields.Date(string="Issued Date")
    return_date = fields.Date(string="Returned Date")
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self: self.env.user.company_id.currency_id)
    fine_amount = fields.Monetary(string="Fine Amount", currency_field='currency_id', compute='_compute_fine_amount',
                                  store=True)
    total_amount = fields.Monetary(string="Total Amount", currency_field='currency_id', compute='_compute_total_amount',
                                   store=True)
    canceled_date = fields.Date(string="Cancel Date")
    cancellation_reason = fields.Char(string="Cancellation Reason")
    borrow_request_lines_ids = fields.One2many('library.borrow.request.line', 'borrow_request_id',
                                               string="Borrow Request Lines")
    days = fields.Integer(string="Days", compute='_compute_days', store=True)

    # @api.depends_context('company')
    # def _compute_company_currency_id(self):
    #     self.currency_id = self.env.company.currency_id

    # @api.model
    # def default_get(self, fields):
    #     defaults = super(BorrowRequest, self).default_get(fields)
    #     if defaults.get('serial_number', 'New') == 'New':
    #         defaults['serial_number'] = self.env['ir.sequence'].next_by_code('borrow.sequence') or 'New'
    #
    #     return defaults


    @api.model_create_multi
    def create(self, vals):
        print('>>>>>>>>>>>>>>>>>>>>>.request')
        for val in vals:
            if val.get('serial_number', 'New') == 'New':
                val['serial_number'] = self.env['ir.sequence'].next_by_code('borrow.sequence') or 'New'
        res = super(BorrowRequest, self).create(vals)
        return res


    def _compute_librarian_id(self):
        for rec in self:
            if rec:
                rec.librarian_id = self.env['res.partner'].search([('user_id', '=', self.env.user.id)]).id
            else:
                rec.librarian_id = False


    def draft_state(self):
        self.state = 'draft'


    def issued_state(self):
        self.state = 'issued'
        for rec in self.borrow_request_lines_ids:
            rec.book_id._compute_available()
            if rec and rec.book_id.available < 0:
                self.state = 'draft'
                raise ValidationError(_(f'"{rec.book_id.name}" BOOK OUT OF STOCK:'))

        self.issued_date = fields.Date.today()


    def returned_state(self):
        self.state = 'returned'
        self.return_date = fields.Date.today()


    def canceled_state(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.wizard',
            'view_mode': 'form',
            'context': {'borrow_request': self.id},
            'target': 'new'
        }


    @api.depends('issued_date', 'return_date')
    def _compute_days(self):
        for rec in self:
            if rec.issued_date and rec.return_date:
                diff = abs(rec.issued_date - rec.return_date)
                rec.days = diff.total_seconds() // (60 * 60 * 24)


    @api.depends('borrow_request_lines_ids.total_amount')
    def _compute_total_amount(self):
        total = 0
        for rec in self:
            if rec.borrow_request_lines_ids:
                for i in rec.borrow_request_lines_ids:
                    total += i.total_amount
                rec.total_amount = total


    @api.depends('borrow_request_lines_ids.fine_amount')
    def _compute_fine_amount(self):
        fine = 0
        for rec in self:
            if rec.borrow_request_lines_ids:
                for i in rec.borrow_request_lines_ids:
                    fine += i.fine_amount
                rec.fine_amount = fine


    def print_receipt(self):
        self.ensure_one()
        return self.env.ref('library_management_urvi.action_report_library_receipt').report_action(self.id)
