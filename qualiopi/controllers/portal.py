# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from operator import itemgetter

from markupsafe import Markup

import logging
from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.osv.expression import OR, AND

_logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        if values.get('sales_user', False):
            values['title'] = _("Salesperson")
        return values

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'training_file_count' in counters:
            values['training_file_count'] = (
                request.env['di.training.file'].search_count(self._prepare_qualiopi_training_file_domain())
                if request.env['di.training.file'].check_access_rights('read', raise_exception=False)
                else 0
            )
        return values

    def _prepare_qualiopi_training_file_domain(self):
        return []

    def _training_file_get_page_view_values(self, training_file, access_token, **kwargs):
        values = {
            'page_name': 'training_file',
            'training_file': training_file,
        }
        return self._get_page_view_values(training_file, access_token, values, 'my_training_file_history', False, **kwargs)

    @http.route(['/my/training_file', '/my/training_file/page/<int:page>'], type='http', auth="user", website=True)
    def my_qualiopi_training_file(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_qualiopi_training_file_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Subject'), 'order': 'name'},
            #'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'reference': {'label': _('Reference'), 'order': 'id'},
            #'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            #'assigned': {'label': _('Assigned'), 'domain': [('user_id', '!=', False)]},
            #'unassigned': {'label': _('Unassigned'), 'domain': [('user_id', '=', False)]},
            #'open': {'label': _('Open'), 'domain': [('close_date', '=', False)]},
            #'closed': {'label': _('Closed'), 'domain': [('close_date', '!=', False)]},
            'last_message_sup': {'label': _('Last message is from support')},
            'last_message_cust': {'label': _('Last message is from customer')},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'id': {'input': 'id', 'label': _('Search in Reference')},
            #'status': {'input': 'status', 'label': _('Search in Stage')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            #'stage': {'input': 'stage_id', 'label': _('Stage')},
        }

        # default sort by value 
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if filterby in ['last_message_sup', 'last_message_cust']:
            discussion_subtype_id = request.env.ref('mail.mt_comment').id
            messages = request.env['mail.message'].search_read([('model', '=', 'di.training.file'), ('subtype_id', '=', discussion_subtype_id)], fields=['res_id', 'author_id'], order='date desc')
            last_author_dict = {}
            for message in messages:
                if message['res_id'] not in last_author_dict:
                    last_author_dict[message['res_id']] = message['author_id'][0]

            training_file_author_list = request.env['di.training.file'].search_read(fields=['id', 'partner_id'])
            training_file_author_dict = dict([(training_file_author['id'], training_file_author['partner_id'][0] if training_file_author['partner_id'] else False) for training_file_author in training_file_author_list])

            last_message_cust = []
            last_message_sup = []
            training_file_ids = set(last_author_dict.keys()) & set(training_file_author_dict.keys())
            for training_file_id in training_file_ids:
                if last_author_dict[training_file_id] == training_file_author_dict[training_file_id]:
                    last_message_cust.append(training_file_id)
                else:
                    last_message_sup.append(training_file_id)

            if filterby == 'last_message_cust':
                domain = AND([domain, [('id', 'in', last_message_cust)]])
            else:
                domain = AND([domain, [('id', 'in', last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                discussion_subtype_id = request.env.ref('mail.mt_comment').id
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search), ('message_ids.subtype_id', '=', discussion_subtype_id)]])
            #if search_in in ('status', 'all'):
            #    search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        # pager
        training_file_count = request.env['di.training.file'].search_count(domain)
        pager = portal_pager(
            url="/my/training_file",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby},
            total=training_file_count,
            page=page,
            step=self._items_per_page
        )

        training_files = request.env['di.training.file'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        #training_files = request.env['di.training.file'].search(domain, order=order, limit=self._items_per_page,)
        request.session['my_training_file_history'] = training_files.ids[:100]

        """if groupby == 'stage':
            grouped_tickets = [request.env['di.training.file'].concat(*g) for k, g in groupbyelem(training_files, itemgetter('stage_id'))]
        else:
            grouped_tickets = [training_files]"""
        #grouped_training_files = [training_files]

        values.update({
            'date': date_begin,
            'training_files': training_files,
            'page_name': 'training file',
            'default_url': '/my/training_file',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return request.render("qualiopi.portal_qualiopi_training_file", values)
    
    @http.route([
        "/qualiopi/training_file/<int:training_file_id>",
        "/qualiopi/training_file/<int:training_file_id>/<access_token>",
        '/my/training_file/<int:training_file_id>',
        '/my/training_file/<int:training_file_id>/<access_token>'
    ], type='http', auth="public", website=True)
    def training_files_followup(self, training_file_id=None, access_token=None, **kw):
        try:
            training_file_sudo = self._document_check_access('di.training.file', training_file_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._training_file_get_page_view_values(training_file_sudo, access_token, **kw)
        return request.render("qualiopi.training_files_followup", values)
    """
    @http.route([
        '/my/ticket/close/<int:ticket_id>',
        '/my/ticket/close/<int:ticket_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def ticket_close(self, ticket_id=None, access_token=None, **kw):
        try:
            ticket_sudo = self._document_check_access('helpdesk.ticket', ticket_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if not ticket_sudo.team_id.allow_portal_ticket_closing:
            raise UserError(_("The team does not allow ticket closing through portal"))

        if not ticket_sudo.closed_by_partner:
            closing_stage = ticket_sudo.team_id._get_closing_stage()
            if ticket_sudo.stage_id != closing_stage:
                ticket_sudo.write({'stage_id': closing_stage[0].id, 'closed_by_partner': True})
            else:
                ticket_sudo.write({'closed_by_partner': True})
            body = _('Ticket closed by the customer')
            ticket_sudo.with_context(mail_create_nosubscribe=True).message_post(body=body, message_type='comment', subtype_xmlid='mail.mt_note')

        return request.redirect('/my/ticket/%s/%s' % (ticket_id, access_token or ''))"""
