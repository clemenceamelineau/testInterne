# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class QualiopiResPartner(models.Model):
    _inherit = "res.partner"
    
    di_siret = fields.Char(string='Siret')
    di_attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    di_internal_company = fields.Boolean('Internal company')