from odoo import api, fields, models

class RentalWizard(models.TransientModel):
    _name = "rental.wizard"
    _description = "Rental Wizard"

    select = fields.Selection([
        ('task_wise','Task wise'),
        ('date_wise','Date wise'),
    ],default="task_wise")
    rental_id = fields.Many2one('rental.order', string="Rental")
    order_ids = fields.One2many(related='rental_id.order_ids', string="Order")
    rent_start_date = fields.Date(string='Start Date')
    rent_end_date = fields.Date(string='End Date')



    def generate_product_bill_using_date(self):
        self.rental_id.update({'state': 'invoiced'})
        l = []
        for i in self.order_ids:
            print("-------1-----------")
            if self.rental_id.rent_start_date >= self.rent_start_date:
                print("-------2-----------")
                if self.rental_id.rent_end_date <= self.rent_end_date:
                    print("-------3-----------")
                    l.append((0, 0, {'name': self.rental_id.customer_id.name, 'quantity': 1, 'price_unit': self.rental_id.total_amount}))

        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.rental_id.customer_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l})

        return {
            'name': self.rental_id.customer_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': res.id,
            'target': self
        }

