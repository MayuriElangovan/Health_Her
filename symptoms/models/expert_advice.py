from odoo import api, fields, models

class ExpertAdvice(models.Model):
    _name = 'expert.advice'
    _inherit = ['mail.thread']
    _description = 'Expert Advice'
    _order = 'id desc'
    _rec_name = 'symptoms_id'
    
    symptoms_id = fields.Many2one('symptoms.symptoms', string='Symptoms')
    symptoms_name = fields.Char(string='Symptoms Name', compute='symptom_name')
    introduction = fields.Text(string='Introduction')
    info_a = fields.Text(string='Information')
    info_b = fields.Text(string='Information')
    info_c = fields.Text(string='Information')
    expert_id = fields.Many2one('res.partner', string ='Expert', domain=[('is_expert','=',True)])
    expert_title = fields.Many2one('res.partner.title', related='expert_id.title', store=True, string="Title")
    expert_position = fields.Char(related='expert_id.function', string="Position", store=True)
    
    @api.depends('symptoms_id')
    def symptom_name(self):
        for record in self:
            if record.symptoms_id:
                record.symptoms_name = str(record.symptoms_id.name) +' ?'
            else:
                record.symptoms_name = 'Symptoms ?'
    
ExpertAdvice()