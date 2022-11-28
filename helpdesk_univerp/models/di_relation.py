# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DIRelation(models.Model):
    _name = "di.relation"
    _description = "Relation"
    
    customer_id = fields.Many2one('res.partner', string='Customer')
    partner_id = fields.Many2one('res.partner', string='Partner',context="{'default_is_company': True, 'show_vat': True, 'default_di_internal_company': True}", domain=[('is_company', '=', True),('di_internal_company', '=', True)])
    code = fields.Text(string='Code')
    
    #Lors de la création / modif d'une relation
    #Cherche le customer_id
    #Ajoute dans le champ 'di_relation_ids' la relation liées