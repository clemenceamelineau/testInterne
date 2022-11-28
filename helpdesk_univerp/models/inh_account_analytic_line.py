# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from math import *
_logger = logging.getLogger(__name__)

class HelpdeskUniverpAccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    
    di_billable = fields.Boolean('Billable', default=True)
    di_activity_id = fields.Many2one('di.time.activity', string='Activity')
    di_time_travel = fields.Float('Travel time', digit=(12,2))
    
    def btn_print(self):
        return self.env.ref('helpdesk_univerp.action_report_intervention_order').report_action(self)
    
    @api.onchange('unit_amount')
    def _onchange_time_spent(self):
        rounding = int(self.env['ir.config_parameter'].sudo().get_param('timesheet_grid.timesheet_rounding', 0))
        min = int(self.env['ir.config_parameter'].sudo().get_param('timesheet_grid.timesheet_min_duration', 0))
        _logger.warning('ROUNDING %s', rounding)
        
        _logger.warning('TEMPS PASSE : %s', self.unit_amount)
        tps = 0.0
        tps = self.unit_amount
        tps = tps * 60 / rounding
        _logger.warning('TPS : %s', tps)
        if tps != 0:
            tps = ceil(tps)
            tps = tps * rounding
            tps = tps * 100 / 60 * 0.01
            _logger.warning('TPS ARR : %s', tps)
            self.unit_amount = tps
    
class HelpdeskUniverpHelpdeskTicketCreateTimesheet(models.TransientModel):
    _inherit="helpdesk.ticket.create.timesheet"
    
    def _default_activity(self):
        _logger.warning(self.ticket_id.name)
        _logger.warning(self.ticket_id.di_project_id.name)
        if self.ticket_id.di_project_id.di_default_activity_id:
            _logger.warning('ACTIVITE %s', self.ticket_id.di_project_id.di_default_activity_id)
            self.di_activity_id = self.ticket_id.di_project_id.di_default_activity_id.id
        else:
            _logger.warning('NONE')
            self.di_activity_id = None
          
          
    di_billable = fields.Boolean('Billable', default=True)
    di_activity_id = fields.Many2one('di.time.activity', string='Activity', default=_default_activity)
    di_time_travel = fields.Float('Travel time', digit=(12,2))
    
      
            
    @api.onchange('time_spent')
    def _onchange_time_spent(self):
        rounding = int(self.env['ir.config_parameter'].sudo().get_param('timesheet_grid.timesheet_rounding', 0))
        min = int(self.env['ir.config_parameter'].sudo().get_param('timesheet_grid.timesheet_min_duration', 0))
        _logger.warning('ROUNDING %s', rounding)
        
        _logger.warning('TEMPS PASSE : %s', self.time_spent)
        tps = 0.0
        tps = self.time_spent
        tps = tps * 60 / rounding
        _logger.warning('TPS : %s', tps)
        if tps != 0:
            tps = ceil(tps)
            tps = tps * rounding
            tps = tps * 100 / 60 * 0.01
            _logger.warning('TPS ARR : %s', tps)
            self.time_spent = tps
                
    
    def action_generate_timesheet(self):
        timesheet = super(HelpdeskUniverpHelpdeskTicketCreateTimesheet, self).action_generate_timesheet()
        
        values = {
            'di_billable': self.di_billable,
            'di_activity_id': self.di_activity_id,
            'project_id': self.ticket_id.di_project_id.id,
            'di_time_travel': self.di_time_travel,
        }
        
        timesheet.update(values)
        return timesheet
    