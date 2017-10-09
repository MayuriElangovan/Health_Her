from odoo import api, fields, models

class SymptomsArticles(models.Model):
    _name = 'symptoms.articles'
    _inherit = ['mail.thread']
    _description = 'Articles'
    _order = 'id desc'
    
    
    
    
    
SymptomsArticles()