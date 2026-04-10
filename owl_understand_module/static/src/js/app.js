// import {registry} from "@web/core/registry";
// import {Component, useState, onWillStart} from "@odoo/owl";
// import {useService} from "@web/core/utils/hooks";
//
// export class Counter extends Component {
//     setup() {
//         this.state = useState({best_score: 0, new_score: 0});
//         this.orm = useService("orm");
//
//         // onWillStart(async () => {
//         //     // const result = await this.orm.searchRead("score.score", [], ["best_score"]);
//         //     const ids = await this.orm.search("score.score", [], ['best_score'])
//         //     if (ids.length > 2){
//         //         let max = ids[0].best_score;
//         //         for (let i = 0; (i < ids.length) -1 ; i++) {
//         //             if (max < ids[i].best_score){
//         //                 max = ids[i].best_score
//         //             }
//         //         }
//         //         this.state.best_score = max;
//         //     }
//         //     else if (ids.length === 1) {
//         //         this.state.best_score = ids.best_score
//         //     }
//         // });
//     }
//
//     async updateScore() {
//         await this.orm.create( "score.score", [{best_score: this.state.new_score}]);
//     }
//
//     increment1() {
//         this.state.new_score += 1;
//     }
//
//     increment2() {
//         this.state.new_score += 2;
//     }
//
//     increment3() {
//         this.state.new_score += 3;
//     }
//
//     decrement5() {
//         if (this.state.new_score < 5) {
//             alert('Cannot be decreased')
//         } else {
//             this.state.new_score = this.state.new_score - 5
//
//         }
//     }
//
//     reset_score() {
//         if (this.state.best_score < this.state.new_score) {
//             this.state.best_score = this.state.new_score;
//             this.updateScore()
//             this.state.new_score = 0;
//         } else {
//             this.state.new_score = 0;
//         }
//     }
// }
//
// Counter.template = "owl_understand_module.Counter";
//
// registry.category("actions").add("owl_understand_module.counter_action", Counter);






