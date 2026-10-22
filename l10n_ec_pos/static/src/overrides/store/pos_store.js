/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import {patch} from "@web/core/utils/patch";
import {PosStore} from "@point_of_sale/app/store/pos_store";
import {makeActionAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {OrderReceipt} from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(PosStore.prototype, {
    /**
     * Override `getReceiptHeaderData` method to add the invoice to the header.
     * @param {*} order
     * @returns
     */
    getReceiptHeaderData(order) {
        const result = super.getReceiptHeaderData(...arguments);
        result.invoice_id = order.get_invoice();
        return result;
    },

    async editPartner(partner) {
        // return super.editPartner(...arguments)
        const record = await makeActionAwaitable(
            this.action,
            "l10n_ec_pos.l10n_ec_res_partner_action_edit_pos",
            // "point_of_sale.res_partner_action_edit_pos",
            {
                props: {resId: partner?.id},
                additionalContext: this.editPartnerContext(),
            }
        );
        const newPartner = await this.data.read("res.partner", record.config.resIds);
        return newPartner[0];
    },
});
