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
# Modificado: las facturas solo muestran y aceptan los diarios permitidos del
# usuario, y la factura nueva ya sale con su diario permitido.
from odoo import api, models


class AccountMove(models.Model):
    """Facturas: solo los diarios permitidos del usuario."""

    _inherit = 'account.move'

    def _get_suitable_journal_ids(self, move_type, company=False):
        """La lista de diarios que se puede elegir en la factura."""
        journals = super()._get_suitable_journal_ids(move_type, company)
        return self.env.user._filter_allowed_journals(journals)

    def _search_default_journal(self):
        """Factura nueva: ya sale elegido el diario permitido del usuario."""
        journal = super()._search_default_journal()
        if journal and not self.env.user._filter_allowed_journals(journal):
            same_type = self.env.user.sudo().allowed_journal_ids.filtered(
                lambda j: j.type == journal.type and j.company_id == journal.company_id
            )
            if same_type:
                return self.env['account.journal'].browse(same_type[:1].id)
        return journal

    @api.constrains('journal_id')
    def _check_user_allowed_journal(self):
        """Error si la factura queda en un diario que el usuario no puede usar."""
        for move in self:
            if move.is_invoice(include_receipts=True):
                self.env.user._check_allowed_journal(move.journal_id)
