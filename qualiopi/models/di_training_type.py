# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class QualiopiTrainingType(models.Model):
    _name = "di.training.type"
    _description = "Type of training"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string = "Name", required = True, translate=True, tracking = True)
    internal_name = fields.Char(string='Internal name', required = True, translate = True, tracking = True)
    partner_id = fields.Many2one('res.partner', string='Default Partner', context="{'default_is_company': True, 'show_vat': True, 'default_di_internal_company': True}", domain=[('is_company', '=', True),('di_internal_company', '=', True)], tracking = True)
    content = fields.Html(string='Content')