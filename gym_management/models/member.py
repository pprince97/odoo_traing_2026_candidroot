from odoo import models, fields, api


class Trainer(models.Model):
    _name = 'gym.member'
    _description = 'Member'

    member = fields.Selection([('trainer', 'Trainer'),('trainee', 'Trainee')], string="Member", readonly=True)
    name = fields.Char(string="Name")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", default='male')
    height = fields.Float(string="Height (cm)")
    weight = fields.Float(string="Weight (kg)")
    dob = fields.Date(string="Date of Birth")
    mobile_no = fields.Char(string="Mobile Number")
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")
    photo = fields.Image(string="Passport Size Photo")

    specialist = fields.Selection(
        [('cardio', 'Cardio'), ('push_ups', 'Push Ups'), ('chest', 'Chest'), ('squats', 'Squats')], string="Specialist",
        default='cardio')
    is_available = fields.Boolean(string="Is Currently Available?", default=True)
    when_available = fields.Selection(
        [('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night')],
        string="When is Available?", default='morning')
    exp_years = fields.Integer(string="Years of Experience")
    bio = fields.Text(string="Bio")

    fitness_goal = fields.Selection([('weight_gain', 'Weight Gain'), ('weight_loss', 'Weight Loss')],
                                    string="Fitness Goal", default='weight_gain')
    shift = fields.Selection(
        [('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night')],
        string="Shift", default='morning')
    is_sub_mem = fields.Boolean(string="Is Subscribed Member?")
    # dummy = fields.Datetime(string="Date of Birth")



