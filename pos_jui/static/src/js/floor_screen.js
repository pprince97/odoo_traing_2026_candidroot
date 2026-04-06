import { patch } from "@web/core/utils/patch";
import { FloorScreen } from "@point_of_sale/app/screens/floor_screen/floor_screen";

patch(FloorScreen.prototype,{
    setup() {
        super.setup();
        this.counter = new Date();
        this.counter.setHours(0, 0, 0, 0);
        this.display = document.getElementById('counter_p');
    },

    startTimer() {
        this.startTime = Date.now(); // Record the exact start moment

        this.timerInterval = setInterval(() => {
            const elapsedMs = Date.now() - startTime;
            this.display.innerText = formatTime(elapsedMs);
        }, 1000); // Update every 1000ms (1 second)
    },

    stopTimer() {
        clearInterval(this.timerInterval); // Stop the counting
        console.log("Final time:", this.display.innerText);
    },

    formatTime(ms) {
        const totalSeconds = Math.floor(ms / 1000);
        const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
        const seconds = (totalSeconds % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    },
})