import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PriceRangeSlider = publicWidget.Widget.extend({
    selector: '#sidebar_view',
    events: {
        'change #slider_range': '_onSliderChange',
    },

    _onSliderChange: function (ev) {
        const value = this.$('#slider_range').val()
        const parts = value.split(',');
        const min = parts[0];
        const max = parts.length > 1 ? parts[1] : parts[0];
        const url = new URL(window.location.href);
        url.searchParams.set('min_price', min);
        url.searchParams.set('max_price', max);
        window.location.assign(url.toString());
    },
});
