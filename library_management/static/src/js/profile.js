/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.UserProfile = publicWidget.Widget.extend({
    selector: '#bookForm',

    start() {
        console.log("Book Form Widget loaded");

//        const modal = document.getElementById("customAlertModal");
//        const openBtn = document.getElementById("submitPopUp");
//        const closeSpan = document.getElementsByClassName("close")[0];
//        const closeButton = document.getElementById("closeAlertButton");
//
//        // Function to display the alert
//        function openCustomAlert() {
//          modal.style.display = "flex";
//        }
//
//        // Function to hide the alert
//        function closeCustomAlert() {
//          modal.style.display = "none";
//        }
//
//        openBtn.addEventListener('click', openCustomAlert);
//
//        closeSpan.addEventListener('click', closeCustomAlert);
//
//        closeButton.addEventListener('click', closeCustomAlert);

//        window.addEventListener('click', function(event) {
//          if (event.target == modal) {
//            closeCustomAlert();
//          }
//        });

//----------------------------------------

//          const alertBox = document.getElementById("customAlertBox");
//          const msg = document.getElementById("alertMessage");
//          const btn = document.querySelector("popup-button");
//          const close = document.querySelector("close");
//
//          btn.addEventListener("click", function() => {
//            alertBox.style.display = "block";
//          });
//
//          close.addEventListener("click", function() => {
//            alertBox.style.display = "none";
//          });


//-------------------------------------------

//        const form = this.el;
//        const alertbox1 = document.getElementById("alertbox1");
//        const alertbox2 = document.getElementById("alertbox2");



//        form.addEventListener("submit", async function (e) {
//            e.preventDefault();
//
//            const formData = new FormData(form);
//
//            try {
//                const response = await fetch("/book-create", {
//                    method: "POST",
//                    body: formData,
//                });
//
//                if (response.ok) {
//                    showAlert(alertbox1, "success");
//                    form.reset();
//                } else {
//                    showAlert(alertbox2, "error");
//                }
//            } catch (error) {
//                showAlert(alertbox2, "error");
//            }
//        });
//
//        function showAlert(box, type) {
//            document.querySelectorAll(".custom-alert").forEach(b => {
//                b.classList.remove("show");
//            });
//
//            box.classList.add("show");
//
//            setTimeout(() => {
//                box.classList.remove("show");
//            }, 4000);
//        }
//
//        return this._super(...arguments);
//    }
});