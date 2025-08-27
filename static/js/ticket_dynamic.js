document.addEventListener("DOMContentLoaded", function () {
    const ticketTypeField = document.getElementById("id_ticket_type");

    const offerFS = document.querySelector(".offer-fieldset");
    const leaveFS = document.querySelector(".leave-fieldset");
    const facilityFS = document.querySelector(".facility-fieldset");
    const advanceFS = document.querySelector(".advance-fieldset");

    function hideAll() {
        [offerFS, leaveFS, facilityFS, advanceFS].forEach(fs => { if (fs) fs.style.display = "none"; });
    }

    function toggleFields() {
        hideAll();
        const value = ticketTypeField.value;
        if (value === "OFFER" && offerFS) offerFS.style.display = "";
        else if (value === "LEAVE" && leaveFS) leaveFS.style.display = "";
        else if (value === "FACILITY" && facilityFS) facilityFS.style.display = "";
        else if (value === "ADVANCE" && advanceFS) advanceFS.style.display = "";
    }

    toggleFields();
    ticketTypeField.addEventListener("change", toggleFields);
});
