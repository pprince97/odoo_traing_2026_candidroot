import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        console.log("Add table timer setup!");
        
        // Initialize timer state
        this.tableTimers = {};
        
        console.log('All tables:', this.tables);
        // Check all tables on load
        if (this.tables && this.tables.length > 0) {
            this.tables.forEach(table => {
                console.log('Checking table on load:', table);
                this.checkAndStartTimer(table);
            });
        }
    },

    startTimer(tableId) {
        console.log('startTimer called for tableId:', tableId);
        
        // Stop existing timer if running
        if (this.tableTimers[tableId]) {
            clearInterval(this.tableTimers[tableId].interval);
        }
        
        let seconds = 0;
        const interval = setInterval(() => {
            const ele = document.querySelector(`.table-timer[data-table-id="${tableId}"]`);
            
            if (!ele) {
                console.warn('Timer element not found for table:', tableId);
                console.log('Available timer elements:', Array.from(document.querySelectorAll('.table-timer')).map(el => ({
                    element: el,
                    tableId: el.getAttribute('data-table-id'),
                    text: el.textContent
                })));
                clearInterval(interval);
                delete this.tableTimers[tableId];
                return;
            }
            
            seconds++;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            
            // Update the element
            if (ele.textContent !== timeStr) {
                ele.textContent = timeStr;
                console.log('Timer updated:', tableId, 'Time:', timeStr);
            }
        }, 1000);
        
        this.tableTimers[tableId] = { interval, seconds };
        console.log('Timer started successfully for table:', tableId);
    },

    async checkAndStartTimer(table) {
        try {
            console.log('Checking table for draft order:', table);
            const hasDraft = await rpc('/pos/has_draft_order', {
                table_id: table.id,
            });
            console.log('Has draft order result:', hasDraft);
            if (hasDraft) {
                console.log('Starting timer for table:', table.table_number);
                // Wait a bit for DOM to be ready, then start timer
                setTimeout(() => {
                    console.log('All timer elements in DOM:', document.querySelectorAll('.table-timer'));
                    this.startTimer(table.id);
                }, 500);
            }
        } catch (e) {
            console.error('Error checking draft order:', e);
        }
    },

    async onClickTable(table, ev) {
        console.log("Table clicked!", table.table_number);
        await this.checkAndStartTimer(table);
        return super.onClickTable(table, ev);
    }
});