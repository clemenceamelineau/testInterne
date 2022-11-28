# -*- coding: utf-8 -*-
from odoo import api, fields, models, modules

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    partner_percent = fields.Float(string="Partner percent", config_parameter="qualiopi.partner_percent")
    training_company_id = fields.Many2one('res.company', string="Training company", config_parameter="qualiopi.training_company_id")
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            partner_percent = self.env['ir.config_parameter'].sudo().get_param('qualiopi.partner_percent'),
            #training_company_id = self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'),
        )

        return res  

    #@api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        _write_partner_percent = self.partner_percent and self.partner_percent or False
        _write_training_company_id = self.training_company_id and self.training_company_id or False

        param.set_param('qualiopi.partner_percent', _write_partner_percent)
        #param.set_param('qualiopi.training_company_id', _write_training_company_id)
        
            