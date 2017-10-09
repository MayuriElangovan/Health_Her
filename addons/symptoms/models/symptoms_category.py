from odoo import api, fields, models

class SymptomsCategory(models.Model):
    _name = 'symptoms.category'
    _inherit = ['mail.thread']
    _description = 'Category'
    _order = 'id desc'
    
    @api.multi
    def _check_category(self):
        exiting_ids = self.search([('name', '=ilike', self.name)])
        if len(exiting_ids) > 1:
            return False
        return True

    _constraints = [(_check_category, 'Category name already exists',['name'])]
    
    name = fields.Char(string='Category')
    symptoms_ids = fields.Many2many('symptoms.symptoms', string='Symptoms')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.uid)
    website_size_x = fields.Integer('Size X', default=1)
    website_size_y = fields.Integer('Size Y', default=1)
    
SymptomsCategory()