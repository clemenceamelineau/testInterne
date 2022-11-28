# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class HelpdeskUniverpProjectProject(models.Model):
    _inherit = "project.project"

    @api.depends('timesheet_ids')
    def _compute_time(self):
        time_total = 0.0
        for project in self:
            for time in self.timesheet_ids:
                _logger.warning('TIME %s', time.name)
                time_total += time.unit_amount
            
            project.update({
                'di_time_total': time_total,
                'di_time_left': project.di_contract_expected_hour - time_total,
                })
            
    def action_show_time_total(self):
        _logger.warning('Ramènera vers les tickets liés ?')
        
        
    allow_timesheets = fields.Boolean(
        "Timesheets", compute='_compute_allow_timesheets', store=True, readonly=False,
        default=False, help="Enable timesheeting on the project.")    
       
    di_internal_company_id = fields.Many2one('res.partner', string='Internal company',context="{'default_is_company': True, 'default_di_internal_company': True}", domain=[('is_company', '=', True),('di_internal_company', '=', True)])
    di_external_project = fields.Char('External project code')
    di_helpdesk_team_id = fields.Many2one('helpdesk.team', string='Helpdesk team')
    di_team_type = fields.Selection([('support', 'Hours contract / Support'),('management', 'Order / Management')], string="Team type", readonly=True, store=True)
    di_contract_is_limited = fields.Boolean('Limited contract', default=False)
    di_contract_expected_hour = fields.Integer('Expected hours (h)', default=9999)
    di_partner_contact_id = fields.Many2one('res.partner', string='Partner contact', context="{'default_is_company': False}", domain=[('is_company', '=', False)])
    di_default_activity_id = fields.Many2one('di.time.activity', string='Default activity')
    di_time_total = fields.Float('Time total', compute='_compute_time')
    di_time_left = fields.Float('Time left', compute='_compute_time')
    di_group_salesperson_id = fields.Many2one('res.users', string='Commercial')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {'domain':{'di_partner_contact_id':[('commercial_company_name', '=', self.partner_id.name),('is_company', '=', False)]}}
    
    @api.onchange('di_helpdesk_team_id')
    def _onchange_helpdesk_team(self):
        if self.di_helpdesk_team_id.di_team_type:
            self.di_team_type = self.di_helpdesk_team_id.di_team_type        
            
    @api.onchange('di_internal_company_id')
    def _onchange_internal_company(self):
        if self.di_internal_company_id.di_group_salesperson_id:
            self.di_group_salesperson_id = self.di_internal_company_id.di_group_salesperson_id
        elif self.di_internal_company_id.di_manager_id:
            self.di_group_salesperson_id = self.di_internal_company_id.di_manager_id
            
        self.di_helpdesk_team_id = None
        return {'domain':{'di_helpdesk_team_id':[('di_internal_company_id', '=', self.di_internal_company_id.id)]}}
     
    @api.onchange('di_contract_is_limited')   
    def _onchange_contract(self):
        if self.di_contract_is_limited == True:
            self.di_contract_expected_hour = 0
        else:
            self.di_contract_expected_hour = 9999
        
        
    
    def write(self, vals):    
        result = super(HelpdeskUniverpProjectProject, self).write(vals) 
        
        if self.active == False:
            ticket_list = self.env['helpdesk.ticket'].search([('di_project_id', '=', self.id)])
            for ticket in ticket_list:
                ticket.stage_id = 3
                  
        
            
        