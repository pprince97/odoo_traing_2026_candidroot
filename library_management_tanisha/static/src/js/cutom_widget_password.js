import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { CharField, charField} from "@web/views/fields/char/char_field";

export class PasswordStrengthField extends CharField {
    static template = "library_management_tanisha.PasswordStrengthField";

    onInput(ev) {
        this.props.record.update({[this.props.name]: ev.target.value});
    }

    get strength() {
        const password = this.props.record.data[this.props.name] || "";

        if (password.length >= 8) {
            const hasLetters = /[a-zA-Z]/.test(password);
            const hasNumbers = /\d/.test(password);
            const hasSpecial = /[@$!%*&#]/.test(password);

            if (hasLetters && hasNumbers && hasSpecial) return "strong";
            if ((hasLetters && hasNumbers) || (hasLetters && hasSpecial) || (hasNumbers && hasSpecial)) return "medium";
        }
        return "weak";
    }

    get inputClass() {
        const password = this.props.record.data[this.props.name] || "";
        if (!password) return "";

        switch (this.strength) {
            case "strong":
                return "o_password_strong";
            case "medium":
                return "o_password_medium";
            default:
                return "o_password_weak";
        }
    }

}

export const passwordStrengthField = {
    ...charField,
    component: PasswordStrengthField,
    displayName: _t("Password Strength"),
    supportedTypes: ["char"],
};

registry.category("fields").add("password_strength", passwordStrengthField);
