/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import {AccountMoveService} from "@account/services/account_move_service";
import {patch} from "@web/core/utils/patch";

patch(AccountMoveService.prototype, {
    /**
     * Added method to get invoice by id.
     * @param invoiceId account_move id
     * @returns {Promise<*>}
     */
    async getInvoice(invoiceId) {
        return await this.orm.searchRead(
            "account.move",
            [["id", "=", invoiceId]],
            [
                "id",
                "name",
                "display_name",
                "move_type",
                "state",
                "invoice_date",
                "l10n_ec_xml_access_key",
            ]
        );
        // return all fields
        // return this.orm.searchRead("account.move", [
        //     ["id", "=", invoiceId],
        // ])
    },
});
