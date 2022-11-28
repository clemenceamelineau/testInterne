# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from _datetime import date, datetime
import logging
from calendar import monthrange
from odoo.exceptions import UserError, Warning
_logger = logging.getLogger(__name__)

class QualiopiDate(models.Model):
    _name = "di.training.date" 
    _description = "Training date"
    _inherit = ['mail.thread', 'mail.activity.mixin']
       
    def _default_start_hours_am(self):
        training_company_id = self.env['res.company'].search([('id', '=', self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'))])
        start_hours_am = 0.0
        start_hours_am = training_company_id.di_hours_start_am
        return start_hours_am 
    
    def _default_end_hours_am(self):
        training_company_id = self.env['res.company'].search([('id', '=', self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'))])
        end_hours_am = 0.0
        end_hours_am = training_company_id.di_hours_end_am
        return end_hours_am 
    
    def _default_start_hours_pm(self):
        training_company_id = self.env['res.company'].search([('id', '=', self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'))])
        start_hours_pm = 0.0
        start_hours_pm = training_company_id.di_hours_start_pm
        return start_hours_pm 
    
    def _default_end_hours_pm(self):
        training_company_id = self.env['res.company'].search([('id', '=', self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'))])
        end_hours_pm = 0.0
        end_hours_pm = training_company_id.di_hours_end_pm
        return end_hours_pm 
    
    
    name = fields.Char(string = "Name", compute="_compute_name")
    training_file_id = fields.Many2one('di.training.file', string="Training File", tracking = True, required = True)
    date = fields.Date(string = "Date", tracking = True, store = True)
    
    date_am = fields.Boolean(string = "Morning", default=True, tracking = True)
    start_hours_am = fields.Float(string= "AM start", default=_default_start_hours_am)
    end_hours_am = fields.Float("AM end", default=_default_end_hours_am)
    
    date_pm = fields.Boolean(string = "Afternoon", default=True, tracking = True)
    start_hours_pm = fields.Float(string= "PM start", default=_default_start_hours_pm)
    end_hours_pm = fields.Float("PM end", default=_default_end_hours_pm)
    
    trainer_day_ids = fields.Many2many('res.partner', string='Trainer', tracking = True, domain=[('is_company', '=', False), ('category_id', '=', 1)])
    trainer_day_name = fields.Char(related = 'trainer_day_ids.name', string = "Trainer name")
    presence_ids = fields.One2many('di.training.presence', 'date_presence', string="Presence")
    comment = fields.Html('Comment')
    
    #Changement du nom 
    @api.depends('date')
    def _compute_name(self):
        for rec in self:
            rec.name = fields.Date.from_string(rec.date).strftime('%d/%m/%Y')
            
    
class QualiopiPresence(models.Model):
    _name = "di.training.presence"
    _description = "Training presence"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string = "Name", compute="_compute_name")
    date_presence = fields.Many2one('di.training.date', string = 'Date', ondelete = 'cascade')
    date_presence_am = fields.Boolean(related="date_presence.date_am", string="Date AM")
    date_presence_pm = fields.Boolean(related="date_presence.date_pm", string="Date PM")
    participant_presence_id = fields.Many2one('res.partner', string='Participants', domain=[('is_company', '=', False)])
    participant_name = fields.Char(related = 'participant_presence_id.name', string = "Participants name", store=True)
    date_am_expected = fields.Boolean(string = "Morning scheduled")
    date_pm_expected = fields.Boolean(string = "Afternoon scheduled")
    date_am_done = fields.Boolean(string="Morning done ?")
    date_pm_done = fields.Boolean(string = "Afternoon done ?")
    training_file_id = fields.Many2one(related = 'date_presence.training_file_id', string="Training File", store=True)

    error_mess = fields.Char(readonly = True, store = True)
    
    #Changement du nom
    @api.depends('date_presence', 'participant_name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.date_presence.name + " - " + rec.participant_name
            
    @api.model
    def create(self, vals):
        present_am = False
        present_pm = False
        error_mess = ""
        
        add_date = self.env['di.training.date'].search([('id', '=', vals['date_presence'])])
        date_ids = self.env['di.training.date'].search([('training_file_id', '!=', add_date.training_file_id.id)])
        participant = self.env['res.partner'].search([('id', '=', vals['participant_presence_id'])])
        _logger.warning('VALS DATE : %s', add_date.name)

        if date_ids:
            for date in date_ids:
                _logger.warning('DATE : %s', date.name)
                if date.name == add_date.name:
                    _logger.warning('DATE TROUVEE')
                    presence = self.env['di.training.presence'].search([('participant_presence_id', '=', vals['participant_presence_id']), ('date_presence', '=', date.id)])
                    if presence:
                        _logger.warning('AM ? %s | PM ? %s', presence.date_am_expected, presence.date_pm_expected)
                        if presence.date_am_expected == True:
                            error_mess += "La personne '" + participant.name + "' est déjà présente sur la formation du " + presence.training_file_id.name + " le matin du " + add_date.name + "\n"
                            present_am = True
                        if presence.date_pm_expected == True:
                            error_mess += "La personne '" + participant.name + "' est déjà présente sur la formation du " + presence.training_file_id.name + " l'après-midi du " + add_date.name + "\n"
                            present_pm = True
    
                        self.error_mess = error_mess
                        _logger.warning('PRESENCE MESS: %s', error_mess)
                        
                training_file = self.env['di.training.file'].search([('id', '=', vals['training_file_id'])])   
    
                _logger.warning('FILE CHERCHE %s', training_file.name)    
                if present_am == False and present_pm == False:
                    _logger.warning('AJOUT DE LA PRESENCE SUR TOUTE LA JOURNEE')
                    return super(QualiopiPresence, self).create(vals)
                
                elif present_am == False:
                    vals['date_pm_expected'] = False
                    _logger.warning('AJOUT DE LA PRESENCE SUR LA MATINEE')
                    training_file.update({
                        'error_comment': training_file.error_comment + error_mess,})
                    return super(QualiopiPresence, self).create(vals)
                
                elif present_pm == False:
                    vals['date_am_expected'] = False
                    _logger.warning('AJOUT DE LA PRESENCE SUR L APREM')
                    training_file.update({
                        'error_comment': training_file.error_comment + error_mess,})
                    return super(QualiopiPresence, self).create(vals)
        else:
            return super(QualiopiPresence, self).create(vals)
                