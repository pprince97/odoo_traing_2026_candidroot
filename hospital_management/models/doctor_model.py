from odoo import models, api, fields, Command


class Doctor(models.Model):
    _name = "hospital.doctor"
    _inherits = {'hr.employee': 'employee_id'}
    _description = "Hospital Doctor"

    name = fields.Char(string="Doctor Name", related="employee_id.display_name", inherited=True, readonly=False)
    employee_id = fields.Many2one('hr.employee', string="Employee", ondelete='cascade', required=True)
    department = fields.Selection([('opd', 'OPD'), ('surgery', 'Surgery'), ('icu', 'ICU')], string="Doctor Department")
    available = fields.Boolean(string="Is Doctor Available")
    room_no = fields.Char(string="Room No")
    max_patients = fields.Integer(string="Max patients")
    doctor_image = fields.Image(string="Doctor Image")
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string="Appointments")
    # skill_ids = fields.Many2many('hr.skill',string="skills",related='employee_id.skill_ids')
    bio = fields.Text(string="Bio")
    d_start = fields.Datetime(default=fields.Datetime.now)
    skill_ids = fields.Many2many('hr.skill')



    @api.model_create_multi
    def create(self, vals):
        res = super(Doctor, self).create(vals)
        for rec in res:
            rec.write({
                'appointment_ids': [
                    Command.create({
                        'name': rec.name,
                        'doctor_id': rec.id,
                        'description': 'command created doctor',
                    }),
                ]
            })
            if rec.employee_id:
                rec.employee_id.approve_doctor()
        return res

    def write(self, vals):
        res = super(Doctor, self).write(vals)
        if vals.get('name'):
            urec = self.env['hospital.appointment'].search([('doctor_id', '=', self.id)])
            self.write({'appointment_ids': [
                Command.update(urec.id, {
                    'name': self.name,
                })
            ]
            })
        # if vals.get('max_patients'):
        #     drec = self.env['hospital.appointment'].search([('doctor_id', '=', self.id)])
        #     self.write({'appointment_ids': [
        #         Command.delete(drec.id)
        #     ]
        #     })
        # if vals.get('bio'):
        #     u_link_rec = self.env['hospital.appointment'].search([('doctor_id', '=', self.id)])
        #     self.write({'appointment_ids': [
        #         Command.unlink(u_link_rec.id)
        #     ]
        #     })
        # if vals.get('room_no'):
        #     u_link_rec = self.env['hospital.appointment'].search([('name', '=', 'doctor link')])
        #     self.write({'appointment_ids': [
        #         Command.link(u_link_rec.id)
        #     ]
        #     })
        # if vals.get('room_no'):
        #     # u_link_rec = self.env['hospital.appointment'].search([('name', '=', 'doctor link')])
        #     self.write({'appointment_ids': [
        #     Command.set([26, 29, 33])
        #     ]
        #     })
        if vals.get('room_no'):
            # u_link_rec = self.env['hospital.appointment'].search([('name', '=', 'doctor link')])
            self.write({'appointment_ids': [
            Command.clear()
            ]
            })
        for rec in self:
            if rec.employee_id:
                rec.employee_id.approve_doctor()
        return res

    def toggle_availability(self):
        if self.available:
            self.available = False
        else:
            self.available = True
