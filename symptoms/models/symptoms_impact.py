from odoo import api, fields, models

class SymptomsImpact(models.Model):
    _name = 'symptoms.impact'
    _inherit = ['mail.thread']
    _description = 'Symptoms Impact'
    _order = 'id desc'
    _rec_name = 'category_id'
    
    partner_id = fields.Many2one('res.partner', string="Partner")
    category_id = fields.Many2one('symptoms.category', string='Category')
    symptoms_line_ids = fields.One2many('symptoms.impact.line','impact_id', string='Symptoms')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.uid)
    
    @api.onchange('category_id')
    def _onchange_category_id(self):
        item_list=[]
        for order in self:
            for categ in order.category_id:
                for symptoms in categ.symptoms_ids:
                    vals = {}
                    vals['symptoms_id'] = symptoms.id
                    vals['category_id'] = order.category_id.id
                    vals['impact_id'] = order.id
                    item_list.append((0, 0, vals))
            order.symptoms_line_ids = item_list
            
SymptomsImpact()

class SymptomsImpactLine(models.Model):
    _name = 'symptoms.impact.line'
    
    impact_id = fields.Many2one('symptoms.impact', string='Category')
    symptoms_id = fields.Many2one('symptoms.symptoms', string='Symptoms')
    category_id = fields.Many2one('symptoms.category', string='Category')
    rating = fields.Integer(string='Rating')
    is_select = fields.Boolean(string="Is Selected ?")
    
    @api.onchange('rating')
    def onchange_rating(self):
        warning={}
        if self.rating < 0 or self.rating > 10:
            warning={'title':'Value Error','message':"Rate the negative impact from 1 to 10"}
        return {'warning':warning}
    
    @api.multi
    def button_info(self):
        context=dict(info_id=self.id)
        return {
            'name': 'Symptom Info',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'symptoms.wizard',
            'target': 'new',
            'context' : context
        }
    
SymptomsImpactLine()    
