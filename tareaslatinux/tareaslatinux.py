# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


class latinuxtarea_tarea(osv.osv):
    """ latinuxtarea """
    _name = 'latinuxtarea.tarea'
    _columns = {
        'user_id': fields.many2one('res.users', 'Creator', required=True, readonly=True),
        'name': fields.char('Task Summary', size=128, required=True, select=True),
        'date_create': fields.date('Create Date', select=True),
        'date_deadline': fields.date('Deadline',select=True),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        'description': fields.text('Description', help='Task contents'),
        'state': fields.selection([('draft', 'New'),('open', 'In Progress'),('pending', 'Pending'), ('done', 'Done'), ('cancelled', 'Cancelled')], 'State', readonly=True, required=True,
                                  help='If the task is created the state is \'Draft\'.\n If the task is started, the state becomes \'In Progress\'.\n If review is needed the task is in \'Pending\' state.\
                                  \n If the task is over, the states is set to \'Done\'.'),
        
    }

    _defaults = {
        'state': lambda *a: 'draft',
        'user_id': lambda obj, cr, uid, context: uid,
        'date_create': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    _order = 'date_create desc'


    def do_open(self, cr, uid, ids, context={}):
        data = {'state': 'open'}
        self.write(cr, uid, ids, data, context=context)
#        self.log(cr, uid, ids, message)
        return True

    def do_draft(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    def onchange_partner_id(self, cr, uid, ids, part=False, context=None):
        partner_obj = self.pool.get('res.partner')
        if not part:
            return {'value':{'contact_id': False}}
        addr = partner_obj.address_get(cr, uid, [part], ['contact'])
        val = {'contact_id': addr['contact']}
        if 'pricelist_id' in self.fields_get(cr, uid, context=context):
            pricelist = partner_obj.read(cr, uid, part, ['property_product_pricelist'], context=context)
            pricelist_id = pricelist.get('property_product_pricelist', False) and pricelist.get('property_product_pricelist')[0] or False
            val['pricelist_id'] = pricelist_id
        return {'value': val}
    
    # def latinuxtarea_cancel(self, cr, uid, ids):
    #     self.write(cr, uid, ids, { 'state': 'cancel' })
    #     return True

    # def latinuxtarea_open(self, cr, uid, ids):
    #     self.write(cr, uid, ids, { 'state': 'open' ,'open_date': time.strftime('%Y-%m-%d %H:%M:%S')})
    #     return True

    # def latinuxtarea_close(self, cr, uid, ids):
    #     self.write(cr, uid, ids, { 'state': 'close' })
    #     return True

    # def latinuxtarea_draft(self, cr, uid, ids):
    #     self.write(cr, uid, ids, { 'state': 'draft' })
    #     return True
    
latinuxtarea_tarea()

class wizard_latinuxtarea_recursos(osv.osv):
    """recursos usados en una tarea """
    _name = 'latinuxtarea.recursos.wizard'
    _columns = {
        'task':fields.many2one('latinuxtarea.tarea','Task'),
        'name_r1':fields.many2one('product.product', 'Product'),
        'quantity_r1':fields.integer('Quantity_r1'),
        'name_r2':fields.many2one('product.product','Product'),
        'quantity_r2':fields.integer('Quantity_r2'),
        'name_r3':fields.many2one('product.product', 'Product'),
        'quantity_r3':fields.integer('Quantity_r3'),
    }

    _defaults = {
        'quantity_r1': lambda *a :0 ,
        'quantity_r2': lambda *a :0,
        'quantity_r3': lambda *a :0,
    }

    def accion(self,cr,uid,ids,context={}):
        return
    
wizard_latinuxtarea_recursos()