from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ReportingBooksHistoryWizard(models.TransientModel):
    _name = 'wizard.reporting.books.history'
    _description = 'Reporting Books History'

    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    is_return_date = fields.Boolean('Is Return Date')
    students_ids = fields.Many2many('res.partner', string='Students')
    books_ids = fields.Many2many('library.books',string='Books')

    def get_history_records(self):
        borrow_requests = self.env['library.borrow.request.lines']
        if not self.is_return_date:
            domain = [
                ('borrow_request_id.state', '!=', 'canceled'),
                '|', ('borrow_request_id.issue_date', '>=', self.start_date),
                ('borrow_request_id.issue_date', '>=', False),
                '|', ('borrow_request_id.return_date', '<=', self.end_date),
                ('borrow_request_id.return_date', '=', False),
            ]
            if self.students_ids:
                domain.append(('borrow_request_id.student_id','in',self.students_ids.ids))
            if self.books_ids:
                domain.append(('book_id','in',self.books_ids.ids))
            report_records = borrow_requests.search(domain)
        else:
            domain = [
                ('borrow_request_id.state', '!=', 'canceled'),
                ('borrow_request_id.return_date', '<=', self.end_date),
                ('borrow_request_id.return_date', '>=', self.start_date),
            ]
            if self.students_ids:
                domain.append(('borrow_request_id.student_id', 'in', self.students_ids.ids))
            if self.books_ids:
                domain.append(('book_id', 'in', self.books_ids.ids))
            report_records = borrow_requests.search(domain)
        return report_records

    def generate_history_report(self):
        return self.env.ref('library_management_rushvi.report_borrow_history').report_action(self)

    @api.onchange('start_date','end_date')
    def _onchange_start_end_date(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_('Start Date must be before End Date'))