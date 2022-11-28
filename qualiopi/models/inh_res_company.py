# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
   
class QualiopiResCompany(models.Model):
    _inherit = "res.company"
    
    di_access_condition = fields.Text(string='Conditions of access')
    di_sanitary_condition = fields.Text(string="Sanitary condition")
    di_hours_start_am = fields.Float(string="Morning")
    di_hours_end_am = fields.Float()
    di_hours_start_pm = fields.Float(string="Afternoon")
    di_hours_end_pm = fields.Float()
    di_representative_id = fields.Many2one('res.partner', string='Representative',  context="{'default_is_company': False}", domain=[('is_company', '=', False)])
    di_goal = fields.Text(string="Goal")
    di_training_manager_id = fields.Many2one('res.partner', string='Training manager', context="{'default_is_company': False}", domain=[('is_company', '=', False)])
    
    di_footer = fields.Html('Footer')
    di_font_color = fields.Char('Font color', default="#FFFFFF")
    di_font_color_text = fields.Char('Font color text', default="#FFFFFF")
    di_background_color = fields.Char('Background color', default="#714b67")
    di_background_color_text = fields.Char('Background color text', default="#714b67")
    
    di_signature = fields.Binary("Signature")
    di_declaration_number = fields.Char("Declaration number")
    di_prefecture = fields.Char("Prefecture")
    
    @api.onchange('di_font_color')
    def _onchange_font_color(self):
        if self.di_font_color:
            self.di_font_color_text = self.di_font_color
            
    @api.onchange('di_font_color_text')
    def _onchange_font_color_text(self):
        if self.di_font_color_text:
            self.di_font_color = self.di_font_color_text
            
    @api.onchange('di_background_color')
    def _onchange_background_color(self):
        if self.di_background_color:
            self.di_background_color_text = self.di_background_color
            
    @api.onchange('di_background_color_text')
    def _onchange_background_color_text(self):
        if self.di_background_color_text:
            self.di_background_color = self.di_background_color_text