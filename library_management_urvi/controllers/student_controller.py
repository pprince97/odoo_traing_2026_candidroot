from odoo import http
from odoo.http import request

class StudentController(http.Controller):

    @http.route(['/student'], type='http', auth="public", website=True)
    def students(self, **kwargs):
        # Fetch all students from your model
        students = request.env['res.partner'].search([('library_role','=','student')])
        return request.render('library_management_urvi.student_listing_page', {
            'students': students
        })