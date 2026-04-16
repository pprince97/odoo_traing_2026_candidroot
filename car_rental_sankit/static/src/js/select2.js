import { loadJS } from "@web/core/assets";
// Inside your widget/component
loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js").then(() => {
    $(".advanced-select").select2({
        placeholder: "Search...",
        allowClear: true,
    });
});
