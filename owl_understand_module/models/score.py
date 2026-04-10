from odoo import models, fields, api

class Score(models.Model):
    _name = 'score.score'
    _description = 'Fetch and Write Score'
    _rec_name = 'best_score'

    best_score = fields.Integer(string='Best score')