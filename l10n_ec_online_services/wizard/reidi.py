import requests

from odoo import _, fields, models


class Reidi(models.TransientModel):
    _name = "one.reidi.wizard"
    _description = "Recover Identification"

    identification = fields.Char(required=True)
    name = fields.Char()
    address = fields.Char()

    def recover(self):
        api_url = "https://reidi.ec.service.resolvedor.dev/entity/"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJyZWlkaS5zZXJ2aWNlLmpvZ3VlbmNvLmRldiIsImlhdCI6MTc0MzgxMTYzMiwiZXhwIjoxNzQ2NDAzNjMyLCJhdWQiOiJqb2d1ZW5jby5kZXYiLCJzdWIiOiJqb3JnZWx1aXNAam9ndWVuY28uZGV2IiwiY2xpZW50IjoiOTk5OTk5OTk5OTk5OSIsIm5hbWUiOiJEZXZlbG9wZXIiLCJlbWFpbCI6ImpvcmdlbHVpc0ByZXNvbHZlZG9yLmRldiIsInJvbGUiOiJkZW1vIiwic2VydmljZSI6IlJlSWRpIiwibGltaXQiOjk5fQ.ElfBlov-dFf_neqC3lTMYnxg6TfxuWtsdu_lPJ03Qpk"

        if self.identification:
            url = f"{api_url}{self.identification}"
            try:
                data = self.make_api_request(url, bearer_token)

                if data:
                    self.name = data.get("name", self.name)
                    self.address = data.get("address", self.address)
                else:
                    return self.message(_("Identification not found or invalid."))
            except Exception as e:
                return self.message(
                    _("Error while fetching data: ") + str(e),
                    type="danger",
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

    def message(self, message, type="warning", title="Warning!"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": type,  # 'success', 'warning', 'danger', 'info'
                "sticky": False,  # Set to True to prevent auto-dismiss
            },
        }

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
