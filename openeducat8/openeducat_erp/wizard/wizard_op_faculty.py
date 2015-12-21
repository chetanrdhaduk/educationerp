# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

from openerp import models, fields, api


class wizard_op_faculty(models.TransientModel):
    _name = 'wizard.op.faculty'
    _description = "Create User the selected Faculty"

    def _get_facultys(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    faculty_ids = fields.Many2many('op.faculty', default=_get_facultys, string='Faculty')

    @api.one
    def create_user(self):
        faculty_pool = self.env['op.faculty']
        user_pool = self.env['res.users']
        user_fields = user_pool.fields_get(self)
        user_default = user_pool.default_get(user_fields)
        user_default_group_lst = user_default['groups_id']
        student_group_id = self.env.ref('openeducat_erp.group_op_faculty').id
        user_default_group_lst[0][2].append(student_group_id)
        user_default['groups_id'] = user_default_group_lst
        active_ids = self.env.context.get('active_ids', []) or []
        for fac in faculty_pool.browse(active_ids):
            if not fac.user_id:
                user_vals = {
                    'name': fac.name,
                    'login': fac.email,
                    'partner_id': fac.partner_id.id
                }
                user_default.update(user_vals)
                user_id = user_pool.create(user_default)
                fac.user_id = user_id


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
