# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv


class avalara_salestax_ping(osv.osv_memory):
    _name = 'avalara.salestax.ping'
    _description = 'Ping Service'

    def default_get(self, cr, uid, fields_list=None, context=None):
        res = super(avalara_salestax_ping, self).default_get(
            cr, uid, fields_list, context)
        self.ping(cr, uid, context=context)
        return res

    _columns = {
        'name': fields.char('Name', size=64),
    }

    def ping(self, cr, uid, context=None):
        """ Call the AvaTax's Ping Service to test the connection. """
        if context is None:
            context = {}

        if context.get('active_id', False):
            avatax_pool = self.pool.get('avalara.salestax')
            avatax_config = avatax_pool.browse(
                cr, uid, context['active_id'], context=context)
            avapoint = avatax_config.get_service()
            # Create 'tax' service for Ping and is_authorized calls
            avapoint.create_tax_service()
            avapoint.ping()
            result = avapoint.is_authorized()
            avatax_pool.write(
                cr, uid, avatax_config.id, {'date_expiration': result.Expires})
        return True
