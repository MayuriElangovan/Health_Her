from odoo import api, fields, models

class SymptomsImpact(models.Model):
    _name = 'symptoms.impact'
    _inherit = ['mail.thread']
    _description = 'Symptoms Impact'
    _order = 'id desc'
    _rec_name = 'category_id'
    
    partner_id = fields.Many2one('res.partner', string="Partner", domain="['|','|',('customer','=',True),('employee','=',True),('supplier','=',True)]", track_visibility='onchange')
    category_id = fields.Many2one('symptoms.category', string='Category', track_visibility='onchange')
    symptoms_line_ids = fields.One2many('symptoms.impact.line','impact_id', string='Symptoms', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.uid, track_visibility='onchange')
    
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


