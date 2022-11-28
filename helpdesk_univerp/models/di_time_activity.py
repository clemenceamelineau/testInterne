# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DITimeActivity(models.Model):
    _name = "di.time.activity"
    _description = "Time Activity"
    
    name = fields.Char('Name')