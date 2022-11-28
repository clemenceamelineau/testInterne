# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from _datetime import date, datetime
import logging
import zipfile
from calendar import monthrange


_logger = logging.getLogger(__name__)

class QualiopiTrainingFile(models.Model):
    _name = "di.training.file"
    _description = "Training File"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #Page sommaire
    name = fields.Char(string = "Name", readonly="True", index=True)
    training_company_id = fields.Many2one('res.company', string="Training company")
    partner_id = fields.Many2one('res.partner', string='Partner', tracking = True, context="{'default_is_company': True, 'show_vat': True, 'default_di_internal_company': True}", domain=[('is_company', '=', True),('di_internal_company', '=', True)], required = True)
    customer_id = fields.Many2one('res.partner', string='Customer', tracking = True, context="{'default_is_company': True, 'show_vat': True}", domain=[('is_company', '=', True)], required = True)
    training_type_id = fields.Many2one('di.training.type', string="Training", tracking = True, required = True)
    date_ids = fields.One2many('di.training.date', 'training_file_id', string="Date", store = True)
    number_days = fields.Float(string = "Number of days", required = True, tracking = True)
    number_hours = fields.Float(string = "Number of hours", required = True, tracking = True)
    sale_order_id = fields.Char(string = "N° Sale Order", required = True,  tracking = True)
    quotation_id = fields.Char(string = "N° Quotation", required = True, tracking = True)
    place = fields.Selection([('place1', 'Customer place'),('place2', 'Partner place'), ('place3', 'Video-conference')], default='place1', string = "Place", tracking = True)
    place_name = fields.Char()
    assigned_to = fields.Many2one('res.users', string='Assigned to', tracking = True, domain=[('is_company', '=', False)], default=lambda self: self.env.user and self.env.user.id or False)

    #Page détail
    #-- Partie assistance commerciale --
    currency_id = fields.Many2one(related="training_company_id.currency_id", string="Currency")
    customer_cost = fields.Monetary(string="Customer Cost")
    partner_cost = fields.Monetary(string="Partner Cost")
    deposit = fields.Monetary(string="Deposit")

    participant_number = fields.Integer(string="Number of participant", tracking = True, required = True)
    sale_code = fields.Char(string="Sale Code", tracking = True)
    admin_contact_id = fields.Many2one('res.partner', string='Administrative Contact', tracking = True,  context={'category_id': 2}, domain=[('category_id', '=', 2)], required = True)
    project_id = fields.Many2one('project.project', string='Project', tracking = True, required = True)
    subrogation_opco = fields.Boolean("Subrogation OPCO ?", default = False, tracking=True)

    #-- Période --
    start_date = fields.Date(string = "Start date", tracking = True)
    end_date = fields.Date(string = "End date", tracking = True)
    last_training_date = fields.Date(string = "Last training date", tracking = True)
    
    start_hours_am = fields.Float(string="Morning", tracking = True)
    end_hours_am = fields.Float(tracking = True)
    start_hours_pm = fields.Float(string="Afternoon", tracking = True)
    end_hours_pm = fields.Float(tracking = True)


    #-- Avant la formation --
    partner_sale_order = fields.Char("Partner sale order", tracking = True)
    purchase_sale_order = fields.Char("Purchase sale order", tracking = True)
    sending_convention_programm = fields.Date("Sending convention and programm", default = False, tracking = True)
    sending_training_document_email = fields.Boolean("Sending training document by email", default = False, tracking = True)
    sending_remote_convocation_email = fields.Boolean("Sending remote convocation by email", default = False, tracking = True)
    sending_convocation_email = fields.Boolean("Sending of the convocation by email", default = False, tracking = True)
    return_agreement_signed = fields.Date("Return of the agreement signed", tracking = True)
    sending_cold_evaluation = fields.Boolean("Sending cold evaluation", default = False, tracking = True)


    #-- Après la formation --
    invoice_status = fields.Selection([('status1', 'To be invoiced'), ('status2', 'Pending'), ('status3', 'Billed')], default = "status1", string = "Invoice status", tracking = True)
    return_evaluation_form = fields.Date("Return evaluation form", tracking = True)
    sending_satisfaction_survey = fields.Date("Sending satisfaction survey", tracking = True)
    return_sign_in_sheet = fields.Date("Return sign-in sheet", tracking = True)
    sending_training_certificate = fields.Date("Sending of the training certificate", tracking = True)


    #Page suivi document
    #-- Dossier du client --
    need_analysis = fields.Boolean("Analysis of the need", default = False, tracking = True)
    need_analysis_date = fields.Date("Date analysis", tracking = True)
    need_analysis_attachment = fields.Binary("Attachment analysis of the need")

    half_day_program = fields.Boolean("Half day program", default = False, tracking = True)
    half_day_program_date = fields.Date("Date program", tracking = True)
    half_day_program_attachment = fields.Binary('Attachment half day program')

    signed_quotation = fields.Boolean("Signed quotation", default = False, tracking = True)
    signed_quotation_date = fields.Date("Date Signed Quotation", tracking = True)
    signed_quotation_attachment = fields.Binary('Attachment signed quotation')

    partner_order = fields.Boolean("Partner order", default = False, tracking = True)
    partner_order_date = fields.Date("Date Partner order", tracking = True)
    partner_order_attachment = fields.Binary('Attachment partner order')

    pedagogical_scenario = fields.Boolean("Pedagogical scenario", default = False, tracking = True)
    pedagogical_scenario_date = fields.Date("Date pedagogical scenario", tracking = True)
    pedagogical_scenario_attachment = fields.Binary('Attachment pedagogical scenario')

    #-- Envoi des documents de formation --
    convocation = fields.Boolean("Convocation", default = False, tracking = True)
    convocation_date = fields.Date("Date convocation", tracking = True)
    convocation_attachment = fields.Binary('Attachment convocation')

    training_agreement = fields.Boolean("Training agreement", default = False, tracking = True)
    training_agreement_date = fields.Date("Date training agreement", tracking = True)
    training_agreement_attachment = fields.Binary('Attachment training agreement')

    completed_program = fields.Boolean("Completed program", default = False, tracking = True)
    completed_program_date = fields.Date("Date completed program", tracking = True)
    completed_program_attachment = fields.Binary('Attachment completed program')

    rules_of_procedure = fields.Boolean("Rules of procedure", default = False, tracking = True)
    rules_of_procedure_date = fields.Date("Date rules of procedure", tracking = True)
    rules_of_procedure_attachment = fields.Binary('Attachment rules of procedure')

    qcm_level_sending = fields.Boolean("QCM of level - Sending", default = False, tracking = True)
    qcm_level_sending_date = fields.Date("Date QCM of level", tracking = True)
    qcm_level_sending_attachment = fields.Binary('Attachment QCM of level - Sending')

    qcm_validation_sending = fields.Boolean("QCM of validation of acquired knowledge - Sending", default = False, tracking = True)
    qcm_validation_sending_date = fields.Date("Date QCM of validation of acquired knowledge", tracking = True)
    qcm_validation_sending_attachment = fields.Binary('Attachment QCM of validation of acquired knowledge - Sending')

    training_registration = fields.Boolean("Training registration forms", default = False, tracking = True)
    training_registration_date = fields.Date("Date training registration forms", tracking = True)
    training_registration_attachment = fields.Binary('Attachment training registration forms')

    training_evaluations = fields.Boolean("Training evaluations - Trainer and trainee", default = False, tracking = True)
    training_evaluations_date = fields.Date("Date training evaluations", tracking = True)
    training_evaluations_attachment = fields.Binary('Attachment training evaluations')

    training_certificates = fields.Boolean("Training certificates", default = False, tracking = True)
    training_certificates_date = fields.Date("Date training certificates", tracking = True)
    training_certificates_attachment = fields.Binary('Attachment training certificates')

    funder_survey = fields.Boolean("Funder survey", default = False, tracking = True)
    funder_survey_date = fields.Date("Date funder survey", tracking = True)
    funder_survey_attachment = fields.Binary('Attachment funder survey')

    #-- Retour des documents de formation --
    training_agreement_signed = fields.Boolean("Training agreement signed", default = False, tracking = True)
    training_agreement_signed_date = fields.Date("Date training agreement signed", tracking = True)
    training_agreement_signed_attachment = fields.Binary('Attachment training agreement signed')

    training_registration_signed = fields.Boolean("Training registration forms signed", default = False, tracking = True)
    training_registration_signed_date = fields.Date("Date training registration forms signed", tracking = True)
    training_registration_signed_attachment = fields.Binary('Attachment training registration forms signed')

    trainee_evaluations = fields.Boolean("Trainee evaluations", default = False, tracking = True)
    trainee_evaluations_date = fields.Date("Date trainee evaluations", tracking = True)
    trainee_evaluations_attachment = fields.Binary('Attachment trainee evaluations')

    trainer_evaluation = fields.Boolean("Trainer evaluation", default = False, tracking = True)
    trainer_evaluation_date = fields.Date("Date trainer evaluation", tracking = True)
    trainer_evaluation_attachment = fields.Binary('Attachment trainer evaluation')

    qcm_level_return = fields.Boolean("QCM of level - Return", default = False, tracking = True)
    qcm_level_return_date = fields.Date("Date QCM of level - Return", tracking = True)
    qcm_level_return_attachment = fields.Binary('Attachment QCM of level - Return')

    qcm_validation_return = fields.Boolean("QCM of validation of acquired knowledge - Return", default = False, tracking = True)
    qcm_validation_return_date = fields.Date("Date QCM of validation of acquired knowledge - Return", default = False, tracking = True)
    qcm_validation_return_attachment = fields.Binary('Attachment QCM of validation of acquired knowledge - Return')

    #-- Commentaire --
    comment_tracking = fields.Text('Commentary')

    #Page Trainers
    trainer_ids = fields.Many2many('res.partner', 'di_training_trainer_ids', string='Trainers', domain=[('category_id', '=', 1)])
    trainer_id_name = fields.Many2many(related='trainer_ids', string='Trainers name')

    #Page participants
    participant_ids = fields.Many2many('res.partner', 'di_training_participant_ids', string='Participants', domain=[('is_company', '=', False)])

    #Page présences
    presence_ids = fields.One2many('di.training.presence', 'training_file_id', string="Presence")
    error_comment = fields.Text('Error')

    #Page commentaire
    comment = fields.Html('Comment')

    @api.model
    def create(self, vals):
        training_company_id = self.env['res.company'].search([('id', '=', self.env['ir.config_parameter'].sudo().get_param('qualiopi.training_company_id'))])

        vals['name'] = self.env['ir.sequence'].next_by_code('di.training.file')
        vals['training_company_id'] = training_company_id.id
        vals['currency_id'] = training_company_id.currency_id
        vals['start_hours_am'] = training_company_id.di_hours_start_am
        vals['end_hours_am'] = training_company_id.di_hours_end_am
        vals['start_hours_pm'] = training_company_id.di_hours_start_pm
        vals['end_hours_pm'] = training_company_id.di_hours_end_pm
        
        """sale_order_obj = self.env['sale.order']
        sale_order = sale_order_obj.create({
            'partner_id': self.env['res.partner'].search([('id', '=', vals['customer_id'])]).id,
            'company_id': self.env['res.partner'].search([('id', '=', vals['partner_id'])]).id,
            })"""
        return super(QualiopiTrainingFile, self).create(vals)

    def btn_presence_clic(self):
        self.error_comment = ""
        #Renseignement du tableau des présences
        if self.date_ids and self.participant_ids:
            for date in self.date_ids:
                _logger.warning("Date : %s | AM : %s | PM : %s", date.name, date.date_am, date.date_pm)
                for participant in self.participant_ids:
                #Ajouter ligne dans le tableau
                    _logger.warning("Participant : %s", participant.name)

                    presence_vals = {
                        'date_presence': date.id ,
                        'participant_presence_id': participant.id,
                        'date_am_expected': date.date_am,
                        'date_pm_expected': date.date_pm,
                        'training_file_id': self.id,
                        }

                    presence_check = self.env['di.training.presence'].search([
                        ('date_presence', '=', date.id),
                        ('participant_presence_id', '=', participant.id),
                        ('training_file_id', '=', self.id),
                        ])
                    if presence_check:
                        am_pm_check = self.env['di.training.presence'].search([
                            ('date_presence', '=', date.id),
                            ('participant_presence_id', '=', participant.id),
                            ('training_file_id', '=', self.id),

                            '|', ('date_am_expected', '!=', date.date_am), ('date_pm_expected', '!=', date.date_pm),
                            ])
                        if am_pm_check:
                            am_pm_check.update({
                                'date_am_expected': date.date_am,
                                'date_pm_expected': date.date_pm,
                                'date_am_done': None,
                                'date_pm_done': None,
                                })
                    else:
                        presence = self.env['di.training.presence'].create(presence_vals)
        
        if self.error_comment != "":
            #Ne refresh pas le tableau
            message = _(self.error_comment)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message,
                    'type': 'warning',
                    'sticky': True,
                    }
                }
        
    #Remplissage de l'entreprise formatrice par défaut lors de la sélection d'une formation
    @api.onchange('training_type_id')
    def _onchange_training_type(self):
        if self.training_type_id:
            self.partner_id = self.training_type_id.partner_id

    #Remplissage du coût pour l'entreprise faisant la formation
    @api.onchange('customer_cost')
    def _onchange_customer_cost(self):

        _partner_percent = self.env['ir.config_parameter'].sudo().get_param('qualiopi.partner_percent')
        _logger.info("partner percent : %s", _partner_percent)
        if _partner_percent and self.customer_cost:
            percent = 1 - float(_partner_percent) * 0.01
            _logger.info("percent : %s", percent)
            self.partner_cost = self.customer_cost * percent
            _logger.info("partner cost : %s", self.partner_cost)

    #Remplissage de l'adresse pour la formation
    @api.onchange('place', 'customer_id', 'partner_id')
    def _onchange_place(self):
        if self.place and self.customer_id and self.partner_id:
            if self.place == 'place1':
                self.place_name = self.customer_id.name + " - " + self.customer_id.zip + " " + self.customer_id.city
                self.place_name = str(self.place_name).upper()

            if self.place == 'place2':

                self.place_name = self.partner_id.name + " - " + self.partner_id.zip + " " + self.partner_id.city
                self.place_name = str(self.place_name).upper()

            if self.place == 'place3':
                if self.customer_id.lang == "fr_FR":
                    self.place_name = "Formation réalisée à distance"
                else:
                    self.place_name = "Distance learning"


    def write(self, vals):
        result = super(QualiopiTrainingFile, self).write(vals)
        
        #Renseignement des dates début, fin et dernière date
        last_date = self.env['di.training.date'].search([
            ('training_file_id', '=', self.id)], order='date desc', limit=1).date

        first_date = self.env['di.training.date'].search([
            ('training_file_id', '=', self.id)], order='date', limit=1).date 
  
        if last_date:
            month_date = last_date.month
            year_date = last_date.year
            day_date = monthrange(year_date, month_date)[1]

            # /!\ Modifier la façon de construire la date /!\
            if month_date < 10 :
                end_date = str(year_date) + "-0" + str(month_date) + "-" + str(day_date)
            else:
                end_date = str(year_date) + "-" + str(month_date) + "-" + str(day_date)

            _logger.info("Dernière date : %s", last_date)
            _logger.info("Jour : %s | Mois : %s | Année : %s", day_date, month_date, year_date)
            _logger.info("Dernier jour du mois : %s", end_date)

            result = super(QualiopiTrainingFile, self).write({
                'last_training_date': last_date,
                'start_date': first_date,
                'end_date': end_date,
                })


    #Remplissage automatique des dates lorsqu'on coche un des champs (suivi des documents)
    @api.onchange('need_analysis', 'half_day_program', 'signed_quotation', 'partner_order', 'pedagogical_scenario', 'convocation', 'training_agreement', 'completed_program', 'rules_of_procedure',
                  'qcm_level_sending', 'qcm_validation_sending', 'training_registration', 'training_evaluations', 'training_certificates', 'funder_survey',
                  'training_agreement_signed', 'training_registration_signed', 'trainee_evaluations', 'trainer_evaluation', 'qcm_level_return', 'qcm_validation_return')
    def _onchange_tracking(self):

        if(self.need_analysis == True):
            if(self.need_analysis_date == False):
                self.need_analysis_date = datetime.today()
        else:
            self.need_analysis_date = None

        if(self.half_day_program == True):
            if(self.half_day_program_date == False):
                self.half_day_program_date = datetime.today()
        else:
            self.half_day_program_date =  None

        if(self.signed_quotation == True):
            if(self.signed_quotation_date == False):
                self.signed_quotation_date = datetime.today()
        else:
            self.signed_quotation_date = None

        if(self.partner_order == True):
            if(self.partner_order_date == False):
                self.partner_order_date = datetime.today()
        else:
            self.partner_order_date = None

        if(self.pedagogical_scenario == True):
            if(self.pedagogical_scenario_date == False):
                self.pedagogical_scenario_date = datetime.today()
        else:
            self.pedagogical_scenario_date = None

        if(self.convocation == True):
            if(self.convocation_date == False):
                self.convocation_date = datetime.today()
        else:
            self.convocation_date = None

        if(self.training_agreement == True):
            if(self.training_agreement_date == False):
                self.training_agreement_date = datetime.today()
        else:
            self.training_agreement_date = None

        if(self.completed_program == True):
            if(self.completed_program_date == False):
                self.completed_program_date = datetime.today()
        else:
            self.completed_program_date = None

        if(self.rules_of_procedure == True):
            if(self.rules_of_procedure_date == False):
                self.rules_of_procedure_date = datetime.today()
        else:
            self.rules_of_procedure_date = None

        if(self.qcm_level_sending == True):
            if(self.qcm_level_sending_date == False):
                self.qcm_level_sending_date = datetime.today()
        else:
            self.qcm_level_sending_date = None

        if(self.qcm_validation_sending == True):
            if(self.qcm_validation_sending_date == False):
                self.qcm_validation_sending_date = datetime.today()
        else:
            self.qcm_validation_sending_date = None


        if(self.training_registration == True):
            if(self.training_registration_date == False):
                self.training_registration_date = datetime.today()
        else:
            self.training_registration_date = None

        if(self.training_evaluations == True):
            if(self.training_evaluations_date == False):
                self.training_evaluations_date = datetime.today()
        else:
            self.training_evaluations_date = None

        if(self.training_certificates == True):
            if(self.training_certificates_date == False):
                self.training_certificates_date = datetime.today()
        else:
            self.training_certificates_date = None

        if(self.funder_survey == True):
            if(self.funder_survey_date == False):
                self.funder_survey_date = datetime.today()
        else:
            self.funder_survey_date = None

        if(self.training_agreement_signed == True):
            if(self.training_agreement_signed_date == False):
                self.training_agreement_signed_date = datetime.today()
        else:
            self.training_agreement_signed_date = None

        if(self.training_registration_signed == True):
            if(self.training_registration_signed_date == False):
                self.training_registration_signed_date = datetime.today()
        else:
            self.training_registration_signed_date = None

        if(self.trainee_evaluations == True):
            if(self.trainee_evaluations_date == False):
                self.trainee_evaluations_date = datetime.today()
        else:
            self.trainee_evaluations_date = None

        if(self.trainer_evaluation == True):
            if(self.trainer_evaluation_date == False):
                self.trainer_evaluation_date = datetime.today()
        else:
            self.trainer_evaluation_date = None

        if(self.qcm_level_return == True):
            if(self.qcm_level_return_date == False):
                self.qcm_level_return_date = datetime.today()
        else:
            self.qcm_level_return_date = None

        if(self.qcm_validation_return == True):
            if(self.qcm_validation_return_date == False):
                self.qcm_validation_return_date = datetime.today()
        else:
            self.qcm_validation_return_date = None


        
        
        