# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2026-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
# Modificado: una validación (constrains) en vez de sobrescribir create y write.
# El create original fallaba si el pago se creaba sin diario (val['journal_id']).
from odoo import api, models


class AccountPayment(models.Model):
    """Pagos: solo en los diarios permitidos del usuario."""

    _inherit = 'account.payment'

    @api.constrains('journal_id')
    def _check_user_allowed_journal(self):
        """Error si el pago queda en un diario que el usuario no puede usar."""
        for payment in self:
            self.env.user._check_allowed_journal(payment.journal_id)
