# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk Univerp',
    'version': '1.1',
    'summary': 'Addon pour adapter le fonctionnement du module Assistance pour le Groupe Univerp',
    'category': '',
    'description': """

""",
    'author': 'Différence informatique - MIADI',
    'depends': [
        'base', 'base_setup', 'helpdesk', 'project', 'hr', 'purchase', 'qualiopi', 'helpdesk_timesheet', 'sale'
        
    ],
    'data': [
        "security/group_user.xml",
        "security/ir.model.access.csv",
        "views/di_time_activity_views.xml",
        "views/di_relation_views.xml",
        "views/inh_project_project_views.xml",
        "views/inh_res_partner_views.xml",
        "views/inh_helpdesk_team_views.xml",
        "views/inh_portal_templates.xml",
        "views/inh_helpdesk_ticket_views.xml",
        "helpdesk_univerp_menu.xml",
        "data/data.xml",
        "data/inh_mail_template_data.xml",
        "reports/helpdesk_univerp_report.xml",
        "reports/intervention_order.xml",
    ],
    
    'demo': [
     ],
     
    'application': False,
    'license': 'OPL-1',
   
  
}
