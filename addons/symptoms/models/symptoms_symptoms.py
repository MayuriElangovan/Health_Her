from odoo import api, fields, models

class SymptomsSymptoms(models.Model):
    _name = 'symptoms.symptoms'
    _inherit = ['mail.thread']
    _description = 'Symptoms'
    _order = 'id desc'
    
    @api.multi
    def _check_symptoms(self):
        exiting_ids = self.search([('name', '=ilike', self.name)])
        if len(exiting_ids) > 1:
            return False
        return True

    _constraints = [(_check_symptoms, 'Symptom name already exists',['name'])]
    
    name = fields.Char(string='Symptoms')
    category_ids = fields.Many2many('symptoms.category', string='Category')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.uid)
    short_desc = fields.Text(string='Symptom Stats')
    detailed_info = fields.Text(string='Symptom Info')
    website_size_x = fields.Integer('Size X', default=1)
    website_size_y = fields.Integer('Size Y', default=1)
    
SymptomsSymptoms()