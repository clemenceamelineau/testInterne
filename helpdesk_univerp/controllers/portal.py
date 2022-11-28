from odoo import http
from odoo.addons.helpdesk.controllers.portal import CustomerPortal  # Import the class
import logging
from odoo.http import request

_logger = logging.getLogger(__name__)

class HelpdeskUniverpCustomerPortal(CustomerPortal):  # Inherit in your custom class

    """@http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
        res = super(HelpdeskUniverpCustomerPortal, self).my_helpdesk_tickets(filterby='open')
        
        return res"""
