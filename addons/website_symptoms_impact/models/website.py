from odoo import models, fields, api

class Website(models.Model):
    _inherit="website"
    
    symptoms_categ_ids = fields.Many2many('symptoms.category', string='Category')
    
Website()