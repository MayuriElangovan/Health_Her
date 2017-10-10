from odoo import models, fields, api, _

class SymptomsWizard(models.TransientModel):
    _name = "symptoms.wizard"

    description = fields.Text(string="Description")

    @api.model
    def default_get(self,fields):
        res = super(SymptomsWizard, self).default_get(fields)
        obj = self.env['symptoms.impact.line'].browse(self._context.get('info_id'))
        for info in obj:
            res.update({'description':info.symptoms_id.description})
        return res
    
SymptomsWizard()
