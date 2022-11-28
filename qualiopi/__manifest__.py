# -*- coding: utf-8 -*-
{
    'name': 'Qualiopi',
    'version': '1.1',
    'summary': 'Qualiopi',
    'category': '',
    'description': """
This module configures your application Qualiopi.
""",
    'author': 'Différence Informatique - MIADI',
    'depends': [
        'base', 'base_setup', 'calendar', 'contacts', 'mail', 'portal', 'sale_management', 'project'
        
    ],
    'data': [
        "data/data.xml",
        "views/inh_parameter_config_views.xml",
        "security/group_user.xml",
        "security/ir.model.access.csv",
        
        "views/di_training_file_views.xml",
        "views/di_training_type_views.xml",
        "views/di_training_date_views.xml",
        "views/inh_res_company_views.xml",
        "views/inh_res_partner_views.xml",
        "views/qualiopi_portal_templates.xml",
        
        "reports/qualiopi_report.xml",
        "reports/achievement_certificate.xml",
        "reports/convocation_training_distance.xml",
        "reports/convocation_training_on_site.xml",
        "reports/eval_customer.xml",
        "reports/eval_participant.xml",
        "reports/eval_trainer.xml",
        "reports/sign_in_sheet_report.xml",
        "reports/training_agreement.xml",
        "reports/training_certificate.xml",
        
        "qualiopi_menu.xml",
    ],
    
    'demo': [
     ],
     
    'application': True,
    'license': 'OPL-1',
   
  
}
