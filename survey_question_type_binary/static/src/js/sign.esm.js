/** @odoo-module **/

import {registry} from "@web/core/registry";
import {SignatureDialog} from "@web/core/signature/signature_dialog";
import {renderToString} from "@web/core/utils/render";
import {templates} from "@web/core/assets";
import {_lt} from "@web/core/l10n/translation";
import {App} from "@odoo/owl";

export const surveySign = {
    dependencies: ["dialog"],
    async start(env, {dialog}) {
        const app = new App(null, {
            templates,
            dev: env.debug,
            translatableAttributes: ["data-tooltip"],
            translateFn: (term) => _lt(term),
            test: false,
        });
        renderToString.app = app;
        // Create and mount dummy app to errors from renderToString
        // which will not enable the signature dialog of auto type
        const dialogProps = {
            defaultName: "Write Your Name",
            fontColor: "DarkBlue",
            mode: "auto",
            displaySignatureRatio: 3,
            signatureType: "signature",
            noInputName: false,
            uploadSignature: (data) => this.uploadSignature(data),
        };
        // Open signature dialog only if its button is mounted to DOM
        const waitForButton = () => {
            const btn = document.getElementById("survey_signature_btn_id");
            if (btn) {
                if (btn.dataset.participantName) {
                    dialogProps.defaultName = btn.dataset.participantName;
                }
                btn.addEventListener("click", () => {
                    dialog.add(SignatureDialog, dialogProps);
                });
            } else {
                setTimeout(waitForButton, 500);
            }
        };

        waitForButton();
        return true;
    },
    uploadSignature({signatureImage}) {
        const data = signatureImage[1];
        const img = document.getElementById("survey_signature_img_id");
        img.src = `data:image/png;base64,${data}`;
        img.style.display = "block";
    },
};

registry.category("services").add("survey_sign", surveySign);
