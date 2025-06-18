import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    api_url = "https://reidi.ec.service.resolvedor.dev/entity/"
    bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJyZWlkaS5zZXJ2aWNlLmpvZ3VlbmNvLmRldiIsImlhdCI6MTc0MzgxMTYzMiwiZXhwIjoxNzQ2NDAzNjMyLCJhdWQiOiJqb2d1ZW5jby5kZXYiLCJzdWIiOiJqb3JnZWx1aXNAam9ndWVuY28uZGV2IiwiY2xpZW50IjoiOTk5OTk5OTk5OTk5OSIsIm5hbWUiOiJEZXZlbG9wZXIiLCJlbWFpbCI6ImpvcmdlbHVpc0ByZXNvbHZlZG9yLmRldiIsInJvbGUiOiJkZW1vIiwic2VydmljZSI6IlJlSWRpIiwibGltaXQiOjk5fQ.ElfBlov-dFf_neqC3lTMYnxg6TfxuWtsdu_lPJ03Qpk"

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
                url = f"{self.api_url}{self.vat}"
                data = self.make_api_request(url, self.bearer_token)

                if data:
                    self.name = data.get("name", self.name)
                    self.street = data.get("address", self.street)

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

    def make_api_request(self, url, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            return False
