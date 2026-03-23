from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class BookHistoryWizard(models.TransientModel):
    _name = 'book.history.wizard'
    _description = 'Book History Wizard'

    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    is_return_date = fields.Boolean(string='Is return date? ')
    student_ids = fields.Many2many(comodel_name='res.partner', relation='book_student_rel', column1='book_borrow_id',column2='student_id', string='Students')
    book_ids = fields.Many2many(comodel_name='library.book', relation='book_borrow_history_rel', column1='book_borrow_id',column2='book_id', string='Books')
    borrow_request_line_ids = fields.Many2many(comodel_name='library.borrow.request.lines', relation='borrow_history_request_line_rel', column1='book_borrow_id',column2='request_line_id', string='Borrow Request Lines')

    def print_history(self):
        domain=[]
        if self.start_date < self.end_date:
            if self.is_return_date:
                domain.extend([('borrow_request_id.state','=','returned'),('return_date','>=',self.start_date),('return_date','<=',self.end_date)])
            else:
                domain.extend([('borrow_request_id.state', '!=', 'canceled'),('issue_date', '>=', self.start_date),('return_date', '<=', self.end_date)])
            if self.student_ids:
                domain.extend([('borrow_request_id.student_id', 'in', self.student_ids.ids)])
            if self.book_ids:
                domain.extend([('book_id', 'in', self.book_ids.ids)])
            self.borrow_request_line_ids = self.env['library.borrow.request.lines'].search(domain)
            return self.env.ref('library_management_tanisha.book_history_report').report_action(self,config=False)
        else:
            raise ValidationError(_("Start date must be less than End Date"))

