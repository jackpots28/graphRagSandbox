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



document.getElementById("clear_btn").addEventListener('click', () => {
    var image = canvas.toDataURL();
    var r = new XMLHttpRequest();
    r.open("POST", "/clear", true);
    r.onreadystatechange = function () {
        if (r.readyState !== 4 || r.status !== 200) return;
        //alert("Success: " + r.responseText);
        console.log("sent");
    };
    // Send data in below way from JS
    r.send(JSON.stringify({"input": "test"}));
});