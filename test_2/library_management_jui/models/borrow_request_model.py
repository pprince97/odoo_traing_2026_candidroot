from odoo import fields, models,api,_
from odoo.exceptions import ValidationError


class BorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow requests'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number', readonly=True)
    student_id = fields.Many2one('res.partner',string='Student',required=True)
    librarian_id = fields.Many2one('res.partner',string='Librarian',compute='_compute_librarian_id',store=True)
    state = fields.Selection([('draft','Draft'),('issued','Issued'),('returned','Returned'),('canceled','Canceled')],string='State', default='draft')
    return_date = fields.Date(string='Return Date')
    issue_date = fields.Date(string='Issue Date')
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount',store=True)
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount',store=True)
    canceled_date = fields.Date(string='Canceled Date')
    cancellation_reason = fields.Char(string='Cancellation Reason')

    borrow_request_lines_id = fields.One2many('library.borrow.request.lines','borrow_request_id',string='Borrow Request Lines')

    def _compute_librarian_id(self):
        self.librarian_id = self.env.user.partner_id

    @api.onchange('state')
    def on_change_state(self):
        if self.state == 'issued':
            self.issued_state()
        elif self.state == 'returned':
            self.returned_state()
        elif self.state == 'canceled':
            self.canceled_state()

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['serial_number'] = self.env['ir.sequence'].next_by_code('borrow.request.seq') or 'New'
        res = super(BorrowRequest, self).create(vals)
        return res

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft','canceled']:
                raise ValidationError(_("You cannot unlink this request"))
            else:
                res=super().unlink()
                return res

    @api.depends('borrow_request_lines_id')
    def _compute_total_amount(self):
        for i in self:
            i.total_amount = 0
            if i.borrow_request_lines_id:
                for rec in i.borrow_request_lines_id:
                    i.total_amount += rec.total_amount

    @api.depends('borrow_request_lines_id')
    def _compute_fine_amount(self):
        for i in self:
            i.fine_amount = 0
            if i.borrow_request_lines_id:
                for rec in i.borrow_request_lines_id:
                    i.fine_amount += rec.fine_amount

    def issued_state(self):
        self.state = 'issued'
        self.issue_date = fields.Date.today()
        for rec in self.borrow_request_lines_id:
            if rec.book_id.available_copies < 0:
                self.state = 'draft'
                raise ValidationError(_(f"{rec.book_id.name} is out of stock"))


    def returned_state(self):
        self.state = 'returned'
        self.return_date = fields.Date.today()
        self._compute_fine_amount()
        self._compute_total_amount()

    def canceled_state(self):
        return {
            'name': 'Borrow request cancel',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'library.borrow.request.cancel.wizard',
            'target': 'new',
            'context': {'default_borrow_request_id': self.id}
        }

    def generate_report(self):
        return self.env.ref('library_management_jui.borrow_request_receipt_action').report_action(self.id)
