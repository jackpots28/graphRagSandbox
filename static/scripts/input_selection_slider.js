const Http = new XMLHttpRequest();
const slider_v = document.getElementById("phrase_count_v");
const output_display_v = document.getElementById("output_p");
let current;

const data: FormData = new FormData()

slider_v.oninput = function() {
    current = this.value
    output_display_v.innerHTML = current
    Http.open('POST', '/')
    Http.send(current)
}

slider_v.oninput = function sendData() {
    current = this.value;

    Http.open('POST', '/')
    Http.send(current)
}