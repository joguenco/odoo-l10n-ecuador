import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.l10n_ec_online_services.utils.http_request import (
    make_api_request,
)

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_default_country(self):
        country = self.env["res.country"].search([("code", "=", "EC")], limit=1)

        return country

    country_id = fields.Many2one(
        "res.country", string="Country", default=_get_default_country
    )

    # @api.constrains("vat", "country_id", "l10n_latam_identification_type_id")
    # def check_vat(self):
    #     result = super().check_vat()
    #     (valid, message) = self.l10n_ec_validate_ci(self.vat)
    #     if not valid:
    #         raise ValidationError(_(message))

    #     return result

    @api.onchange("vat")
    # pylint: disable=W8110
    def onchange_vat(self):
        self.ensure_one()
        if self.vat and self.country_id.code == "EC":
            is_valid_identification = False
            if self._l10n_ec_get_identification_type() == "cedula":
                super().check_vat()
                (valid, message) = self.l10n_ec_validate_ci(self.vat)
                if not valid:
                    raise ValidationError(_(message))
                is_valid_identification = True
            elif self._l10n_ec_get_identification_type() == "ruc":
                if self.vat:
                    super().check_vat()
                    is_valid_identification = True

            # Query identification
            if is_valid_identification:
                use_reidi = (
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("l10n_ec_online_services.use_reidi")
                )
                if use_reidi:
                    api_url = (
                        self.env["ir.config_parameter"]
                        .sudo()
                        .get_param("l10n_ec_online_services.reidi_api_url")
                    )
                    bearer_token = (
                        self.env["ir.config_parameter"]
                        .sudo()
                        .get_param("l10n_ec_online_services.reidi_bearer_token")
                    )
                    url = f"{api_url}/entity/{self.vat}"
                    try:
                        data = make_api_request(url, bearer_token)
                    except Exception as e:
                        _logger.error(f"Error making API request to {url}: {e}")

                    if data:
                        self.name = data.get("name", self.name)
                        self.street = data.get("address", self.street)
                    else:
                        self.name = False
                        self.street = False

    def l10n_ec_validate_ci(self, identification) -> tuple[bool, str]:
        province = int(identification[0:2])  # dos primeros dígitos de la CI
        if 1 <= province <= 24 or province == 30:
            third_digit = int(identification[2])
            # El tercer dígito debe estar entre 0 y 6
            if 0 <= third_digit <= 6:
                validator = int(identification[9])
                coefficients = (2, 1, 2, 1, 2, 1, 2, 1, 2)  # coeficientes del módulo 10
                accumulated = 0
                for i in range(0, len(coefficients)):
                    multiplication = int(identification[i]) * coefficients[i]
                    # Si una multiplicación es >= 10 se le debe restar 9
                    if multiplication >= 10:
                        multiplication -= 9
                    # print(f'Digito {int(cedula[i])}, multiplicacion {multip}')
                    accumulated += multiplication
                module = accumulated % 10  # calculamos el módulo 10
                subtract = (
                    10 - module
                )  # para calcular el validador restamos de 10 el módulo obtenido

                if subtract == validator or (module == 0 and validator == 0):
                    return True, "La cédula es válida"
                else:
                    return False, "La cédula no es válida"
            else:
                return False, "El tercer dígito no es válido"
        else:
            return False, "El código de provincia no es válido"
