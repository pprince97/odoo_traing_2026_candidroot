from odoo import Command, models, fields, api


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Doctor Name')
    department = fields.Selection([('opd', 'OPD'), ('surgery', 'Surgery'), ('icu', 'ICU')], string='Department',
                                  default='opd')
    available = fields.Boolean(string='Available', default=True)
    room_no = fields.Integer(string='Room Number')
    max_patients = fields.Integer(string='Maximum Patients')
    doctor_img = fields.Image(string='Doctor Image')
    bio = fields.Text(string='Bio')
    current_date = fields.Date(string='Current Date', default=fields.Datetime.today())
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')
    doctor_count = fields.Integer()


    @api.model_create_multi
    def create(self, vals):
        res = super(Doctor, self).create(vals)
        # --------------------Command.create-------------------------
        # for rec in res:
        #     print('rec---------------------------------', rec)
        #     rec.write({
        #         'appointment_ids': [Command.create({
        #             'name': rec.name,
        #             'doctor_id': rec.id,
        #             'description': "record created",
        #         })],
                # 'appointment_ids': [(0, 0, {
                #     'name': rec.name,
                #     'doctor_id': rec.id,
                #     'description': "record created",
                # })],
            # })
        return res

    def write(self, vals):
        res = super(Doctor, self).write(vals)
        # --------------------Command.write-------------------------
        if vals.get('name'):
            print("vals-----------------------------", vals)
            print("self_id-----------------------------", self.id)
            # for _id in self.appointment_ids.ids:
            #     print("rec------------------------------", )
            #     self.write({
            #         'appointment_ids': [Command.update(_id, {
            #             'name': self.name,
            #             'doctor_id': self.id,
            #         })]
                    # 'appointment_ids': [(1, _id, {
                    #     'name': self.name,
                    #     'doctor_id': self.id,
                    # })]
                # })
                # print("id---------------------------------", self.appointment_ids.id)

                # --------------------Command.delete-------------------------
                # if not self.available:
                #     self.write({
                #         'appointment_ids': [Command.delete(_id)]
                #     })
                # self.write({
                #     'appointment_ids': [(2, _id, 0)]
                # })

                # --------------------Command.unlink-------------------------
                # if not self.available:
                #     self.write({
                #         'appointment_ids': [Command.unlink(_id)]
                #     })
                # self.write({
                #     'appointment_ids': [(3, _id, 0)]
                # })

            # --------------------Command.link-------------------------
            # if self.available:
            # self.write({
            #    'appointment_ids': [Command.link(10)]
            # })
            # self.write({
            #     'appointment_ids': [(4, 10, 0)]
            # })

            # --------------------Command.clear-------------------------
            # if not self.available:
            #     self.write({
            #        'appointment_ids': [Command.clear()]
            #     })
            # self.write({
            #     'appointment_ids': [(5, 0, 0)]
            # })

            # --------------------Command.set-------------------------
            # if self.available:
            # self.write({
            #    'appointment_ids': [Command.set([39, 14, 11])]
            # })
            # self.write({
            #     'appointment_ids': [(6, 0, [1, 27, 24])]
            # })

        return res

    def toggle_availability(self):
        self.available = not self.available

    def approve_doctor(self):
        print("Approve doctor")
        self.doctor_count = self.env['hospital.doctor'].search_count([('available', '=', True)])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.doctor',
            'view_mode': 'list,form',
            'domain': [('available', '=', True)]
        }

