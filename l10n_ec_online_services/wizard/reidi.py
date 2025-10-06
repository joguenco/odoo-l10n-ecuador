from odoo import _, fields, models

# pylint: disable=W8150
from odoo.addons.l10n_ec_online_services.utils.http_request import (
    make_api_request,
)


class Reidi(models.TransientModel):
    _name = "one.reidi.wizard"
    _description = "Recover Identification"

    identification = fields.Char()
    name = fields.Char()
    address = fields.Char()

    def recover(self):
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

            if self.identification:
                url = f"{api_url}/entity/{self.identification}"
                try:
                    data = make_api_request(url, bearer_token)

                    if data:
                        self.name = data.get("name", self.name)
                        self.address = data.get("address", self.address)
                    else:
                        return self.message(_("Identification not found or invalid."))
                except Exception as e:
                    return self.message(
                        _("Error while fetching data: ") + str(e),
                        type_of="danger",
                        title="Error!",
                    )
            else:
                return self.message(_("Please enter an identification."))

            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "one.reidi.wizard",
                "target": "new",
                "name": "Recover Identification - ReIdi",
                "res_id": self.id,
            }

        return self.message(_("ReIdi service is inactive."))

    def message(self, message, type_of="warning", title="Warning!"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": type_of,  # 'success', 'warning', 'danger', 'info'
                "sticky": False,  # Set to True to prevent auto-dismiss
            },
        }
