from odoo import models,fields,api,Command

class LibraryBorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow Request'
    _rec_name = 'serial_no'


    serial_no = fields.Char(string='Serial number')
    student_id = fields.Many2one(comodel_name='res.partner',string='Student')
    librarian_id = fields.Many2one(comodel_name='res.partner',string='Librarian')
    state = fields.Selection([('draft', 'Draft'),('issued', 'Issued'),('returned', 'Returned'),('canceled', 'Canceled')],string='State',default='draft')
    issue_date = fields.Date(string='Issue date')
    return_date = fields.Date(string='Return date')
    fine_amount = fields.Float(string='Fine amount')
    total_amount = fields.Float(string='Total amount')
    canceled_date = fields.Date(string='Canceled date')
    cancellation_reason = fields.Text(string='Cancellation reason')
    borrow_request_line_ids = fields.One2many(comodel_name='library.borrow.request.lines',inverse_name='borrow_request_id')

    @api.model_create_multi
    def create(self, vals_list):
        vals_list[0]['serial_no'] = self.env['ir.sequence'].next_by_code('borrow.request.seq') or 'New'
        res = super(LibraryBorrowRequest, self).create(vals_list)
        # res_user = self.env['res.users'].context_get()
        # res_partner = self.env['res.users'].browse(res_user['uid']).partner_id
        # print("--------------------------------",res_partner.id)
        # for rec in res:
        #     rec.write({
        #         'librarian_id': [Command.set(res_partner.id)]
        #     })
        return res

    def state_draft(self):
        self.state = 'draft'

    def state_issue(self):
        self.state = 'issued'
        self.issue_date = fields.Date.today()

    def state_returned(self):
        self.state = 'returned'
        self.return_date = fields.Date.today()
        ref_fine_amount = self.env['ir.config_parameter'].sudo().get_param('fine_amount')
        for borrow_request_line in self.borrow_request_line_ids:
            if borrow_request_line.return_date < self.return_date:
                borrow_request_line.fine_amount = (self.return_date - borrow_request_line.return_date).days*float(ref_fine_amount)
            else:
                borrow_request_line.fine_amount = 0
        for rec in self:
            self.fine_amount = sum(rec.borrow_request_line_ids.mapped('fine_amount'))
            self.total_amount = sum(rec.borrow_request_line_ids.mapped('total_amount'))

    def state_canceled(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'request.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'cancel_wizard': self.id}
        }

