# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class HelpdeskUniverpHelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    di_internal_company_id = fields.Many2one('res.partner', domain=[('di_internal_company', '=', True)], context="{'default_di_internal_company': True}")
    di_team_type = fields.Selection([('support', 'Hours contract / Support'),('management', 'Order / Management')], string="Team type")

    assign_method = fields.Selection([
        ('manual', 'Manual'),
        ('randomly', 'Random'),
        ('balanced', 'Balanced')], string='Assignment Method', default='manual',
        required=True, help='Automatic assignment method for new tickets:\n'
             '\tManually: manual\n'
             '\tRandomly: randomly but everyone gets the same amount\n'
             '\tBalanced: to the person with the least amount of open tickets', readonly=True)

    privacy = fields.Selection([
        ('user', 'All Users'),
        ('invite', 'Invited Users')],
        string="Users Assign", default="invite")
    
    use_helpdesk_timesheet = fields.Boolean(
        'Timesheets', compute='_compute_use_helpdesk_timesheet',
        store=True, readonly=True, help="This requires to have project module installed.", default=True)
