# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class HelpdeskUniverpResPartner(models.Model):
    _inherit = "res.partner"

    di_default_contract_id = fields.Many2one('project.project', string='Default contract', tracking=True)
    di_default_company_id = fields.Many2one('res.partner', string='Default company', context="{'default_is_company': True, 'default_di_internal_company': True}", domain=[('is_company', '=', True),('di_internal_company', '=', True)], tracking=True)
    di_manager_id = fields.Many2one('res.users', string='Manager', context="{'default_type': 'contact'}", tracking=True)
    di_group_salesperson_id = fields.Many2one('res.users', string='Commercial', context="{'default_type': 'contact'}", tracking=True)
    di_relation_ids = fields.Many2many('di.relation', string='Relations')

    @api.onchange('di_default_contract_id')
    def _onchange_default_contract(self):
        if self.di_default_contract_id.di_internal_company_id:
            self.di_default_company_id = self.di_default_contract_id.di_internal_company_id

    @api.onchange('di_manager_id', 'di_group_salesperson_id')
    def _onchange_manager_commercial(self):
        if self.di_manager_id == self.di_group_salesperson_id:
            self.di_group_salesperson_id = None
            _logger.warning('MANAGER = COMMERCIAL')
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'The manager and the commercial are identical.\nSuppression of the commercial',
                    'type': 'warning',
                    'sticky': False,
                    }
            }
