# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


def days_between(d1, d2):
    d1 = fields.Datetime.from_string(d1)
    d2 = fields.Datetime.from_string(d2)
    return abs((d2 - d1).days)


class OpBookMovement(models.Model):
    _name = 'op.book.movement'
    _rec_name = 'book_id'

    book_id = fields.Many2one('op.book', 'Book', required=True)
    quantity = fields.Integer('No. Of Books', required=True)
    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')], 'Student/Faculty',
        required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    library_card_id = fields.Many2one(
        'op.library.card', 'Library Card', required=True)
    issued_date = fields.Date('Issued Date', required=True)
    return_date = fields.Date('Return Date', required=True)
    actual_return_date = fields.Date('Actual Return Date')
    penalty = fields.Float('Penalty')
    partner_id = fields.Many2one('res.partner', 'Person')
    reserver_name = fields.Char('Person Name', size=256)
    state = fields.Selection(
        [('i', 'Issued'), ('a', 'Available'), ('l', 'Lost'),
         ('r', 'Reserved')], 'Status', default='a')

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        if self.issued_date > self.return_date:
            raise ValidationError(
                _("Issue Date Should be greater than Return Date."))
            
#     @api.constrains('quantity')
#     def _check_number_book(self):
#           move_total_book = 0
#           for rec in self.book_id:
#              for move_id in rec.movement_line:
#                     move_total_book += move_id.quantity
#              if rec.number_book < move_total_book:
#                      raise ValidationError(
#                     _("This Book not Available"))
                     
    @api.onchange('book_id')
    def onchange_book_id(self):
        self.state = self.book_id.state

    @api.one
    def issue_book(self):
        ''' function to issue book '''
        move_total_book = 0
        for rec in self.book_id:
           for move_id in rec.movement_line:
               if move_id.state == 'i':
                  move_total_book += move_id.quantity
           if rec.number_book < move_total_book  :
                   raise ValidationError(
                  _("This Book not Available"))
           if rec.number_book >= (move_total_book + self.quantity) : 
               #if self.book_id.state and self.book_id.state == 'a':
                self.book_id.state = 'i'
                self.state = 'i'
           else:
                   raise ValidationError(
                  _("This Book not Available"))
    @api.one
    def calculate_penalty(self):
        penalty_amt = 0
        penalty_days = 0
        standard_diff = days_between(self.return_date, self.issued_date)
        actual_diff = days_between(self.actual_return_date, self.issued_date)
        owned_days = standard_diff + \
            self.library_card_id.library_card_type_id.duration
        if self.library_card_id and self.library_card_id.library_card_type_id:
            penalty_days = actual_diff > owned_days and actual_diff - \
                owned_days or penalty_days
            penalty_amt = round(penalty_days - penalty_days / 7) * \
                self.library_card_id.library_card_type_id.penalty_amt_per_day
        self.write({'penalty': penalty_amt, 'state': 'a'})
        self.book_id.state = 'a'

    @api.multi
    def return_book(self):
        ''' function to return book '''
        if self.book_id.state and self.book_id.state == 'i':
            return {
                'name': _('Return Date'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'return.date',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        return True

    @api.multi
    def do_book_reservation(self):
        ''' function to reserve book '''
        return {
            'name': _('Book Reservation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'reserve.book',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
