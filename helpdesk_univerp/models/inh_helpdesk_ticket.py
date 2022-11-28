# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class HelpdeskUniverpHelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    
    project_id = fields.Many2one("project.project", related="di_project_id", readonly=True, store=True)
    
    di_project_id = fields.Many2one('project.project', string='Business / Contract')
    di_internal_company_id = fields.Many2one('res.partner', related='di_project_id.di_internal_company_id', string='Internal company')
    di_contact = fields.Many2one('res.partner', string='Contact', domain=[('is_company', '=', False)], context="{'default_is_company': False}")
    di_contract_expected_hour = fields.Integer(related='di_project_id.di_contract_expected_hour', string='Expected hours (h)')
    di_contract_time_total = fields.Float(related='di_project_id.di_time_total', string='Contract time total')
    di_contract_time_left = fields.Float(related='di_project_id.di_time_left', string='Contract time left')
    
    di_time_total = fields.Float('Time total', store=True)
    di_time_total_billable = fields.Float('Time total billable')
    di_time_total_no_billable = fields.Float('Time total not billable')
    di_previous_ticket = fields.Many2one('helpdesk.ticket', string='Previous ticket', readonly = True)
    
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', index=True, required = True)
    
    @api.onchange('timesheet_ids')
    def _onchange_timesheet(self):
        total_billable = 0.0
        total_no_billable = 0.0
        for ticket in self:
            _logger.warning('TICKET %s', ticket.name)
            for time in self.timesheet_ids:
                _logger.warning('TIME %s', time.name)
                if time.di_billable == True:
                    total_billable += time.unit_amount
                else:
                    total_no_billable += time.unit_amount
                    
            ticket.update({
                'di_time_total_billable': total_billable,
                'di_time_total_no_billable': total_no_billable,
                })
            
                
    
    @api.onchange('di_project_id')
    def _onchange_project_id(self):
        if self.di_project_id:
            self.team_id = self.di_project_id.di_helpdesk_team_id
            if self.di_project_id.di_partner_contact_id:
                self.di_contact = self.di_project_id.di_partner_contact_id
                if self.di_contact.email:
                    self.partner_email = self.di_contact.email
                if self.di_contact.phone:
                    self.partner_phone = self.di_contact.phone
            else:
                self.di_contact = None
                self.partner_email = self.partner_id.email
                self.partner_phone = self.partner_id.phone
            
    @api.onchange('di_contact')
    def _onchange_contact_id(self):
        if self.di_contact:
            if self.di_contact.email:
                self.partner_email = self.di_contact.email
            if self.di_contact.phone:
                self.partner_phone = self.di_contact.phone
            
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.di_project_id = self.partner_id.di_default_contract_id
        self.di_contact = None
        return {'domain':{'di_contact':[('commercial_company_name', '=', self.partner_id.name),('is_company', '=', False)]}}
    

    def write(self, vals):
        
        if self.stage_id.is_close == True:
            raise UserError(_("The ticket is closed and cannot be modified."))
        
        
        result = super(HelpdeskUniverpHelpdeskTicket, self).write(vals)
    
    @api.model
    def create(self, vals):
        result = super(HelpdeskUniverpHelpdeskTicket, self).create(vals)
        for record in result:
            followers=[]
            notification_ids = []
            if record.di_internal_company_id.di_manager_id.id:
                followers.append(record.di_internal_company_id.di_manager_id.partner_id.id)
                
            if record.di_project_id.di_group_salesperson_id.id:
                followers.append(record.di_project_id.di_group_salesperson_id.partner_id.id)
                
            elif record.di_internal_company_id.di_group_salesperson_id.id:
                followers.append(record.di_internal_company_id.di_group_salesperson_id.partner_id.id)
               
            record.message_subscribe(partner_ids = followers)
            
            record._portal_ensure_token()
            
        return result
    
    def _cancel_and_duplicate(self):
        _logger.warning('CANCEL AND DUPLICATE')
        self.stage_id = 4
        new_ticket = self.copy({'di_previous_ticket': self.id,'di_time_total_billable': 0.0, 'di_time_total_no_billable': 0.0})
        _logger.warning('ID : %s | NAME : %s', new_ticket.id, new_ticket.name)
        
        
        
        view_id = self.env["ir.model.data"].check_object_reference("helpdesk", "helpdesk_ticket_view_form", True)
        return {"type":"ir.actions.act_window",
                "view_mode":"form",
                "view_type":"form",
                "views":[(view_id[1], "form")],
                "res_id":new_ticket.id,
                "target":"current",
                "res_model":"helpdesk.ticket",       
                }
    
        
class HelpdeskUniverpHelpdeskStage(models.Model):
    _inherit = "helpdesk.stage"
    
    commercial_template_id = fields.Many2one(
        'mail.template', 'Commercial Email Template',
        domain="[('model', '=', 'helpdesk.ticket')]",
        help="Automated email sent to the project's commercial when the ticket reaches this stage.")
    
    
    
    
    
    
    