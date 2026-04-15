from odoo import api, fields, models,Command

class VehicleDriver(models.Model):
    _inherit = "res.partner"

    is_customer = fields.Boolean(string="Customer")
    is_driver = fields.Boolean(string="Is Driver")
    licence_no = fields.Char(string="Licence Number",required=True)
    licence_document = fields.Binary(string="Licence Document",attachment=True)
    file_name = fields.Char(string="File Name")
    status = fields.Boolean(string="Status",default=True)
    driver_per_day_rate = fields.Float(string="Driver per Day Rate",required=True)
    booking_line_ids = fields.One2many('vehicle.booking.line','driver_id',string="Booking Lines")
    booking_history_count = fields.Integer(string="Booking History Count")

    def booking_history(self):
        records = self.env['vehicle.booking.line']
        self.booking_history_count = records.search_count([
            ("driver_id", "=", self.id),
        ])
        return {
            'name': "Booking History",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'vehicle.booking.line',
            'target': 'self',
            'domain': [
                ("driver_id", "=", self.id),
            ],
        }

    @api.model_create_multi
    def create(self, vals):
        res = super(VehicleDriver,self).create(vals)
        for rec in res:
            if rec and rec.is_customer == True:
                user = self.env['res.users']
                user_id = user.create(
                    {'name': rec.name, 'login': rec.name, 'email': rec.email, 'partner_id': rec.id, 'password': 'admin',
                     'group_ids': [Command.set([self.env.ref('base.group_portal').id])]})
                rec.update({'user_id': user_id.id})
        return res