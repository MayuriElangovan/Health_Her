from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    @api.depends('impact_ids.partner_id')
    def _get_symptom_ids(self):
        for order in self:
            symp_obj = self.env['symptoms.impact'].search([('partner_id','=',order.id)])
            order.impact_ids = [(4, symp.id) for symp in symp_obj]
            
    impact_ids = fields.Many2many('symptoms.impact','partner_impact_rel', 'partner_id', 'impact_id', compute = '_get_symptom_ids', string="Impact")
    is_expert = fields.Boolean(string='Is Expert?')
    
ResPartner()