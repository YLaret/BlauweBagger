const currentPath = window.location.pathname;

const navlinkoverview = document.querySelector('#nav-link-overview');
const navlinktableview = document.querySelector('#nav-link-tableview');
const navlinkprogram = document.querySelector('#nav-link-program');

if (currentPath == "/")
{
    navlinkoverview.classList.add('active')
    navlinktableview.classList.remove('active')
    navlinkprogram.classList.remove('active')
} else if (currentPath == "/tableview") {
    navlinkoverview.classList.remove('active')
    navlinktableview.classList.add('active')
    navlinkprogram.classList.remove('active')
} else if (currentPath == "/program") {
    navlinkoverview.classList.remove('active')
    navlinktableview.classList.remove('active')
    navlinkprogram.classList.add('active')
}

/*
function updatePage() {
            fetch('/updatepage')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("program-run-time").innerText = data.programRunTime
                    const meters = document.getElementsByClassName("meters");
                    for (let i = 0; i < meters.length; i++) {
                        meters.item(i).innerText = data.meters[i];
                    }
                    const switches = document.getElementsByClassName("switch-btn")
                    if (data.activeSwitches) {
                        for (let i = 0; i < switches.length; i++) {
                            const id = parseInt(switches.item(i).id)
                            if (data.activeSwitches && data.activeSwitches.includes(id)) {
                                switches.item(i).classList.add("switch-active")
                                console.log
                            } else {
                                switches.item(i).classList.remove("switch-active")
                            }
                        }
                    }
                    /*let meter = document.getElementById("meter");
                    meter.value = data.reading;
                    document.getElementById("meter_value").innerText = data.reading;
                })
                .catch(error => console.error('Error fetching meter reading:', error));
        }
*/
function updatePage() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/updatepage", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            document.getElementById("program-run-time").innerText = data.programRunTime;

            var meters = document.getElementsByClassName("meters");
            for (var i = 0; i < meters.length; i++) {
                meters[i].innerText = data.meters[i];
            }

            var switches = document.getElementsByClassName("switch-btn");
            if (data.activeSwitches) {
                for (var i = 0; i < switches.length; i++) {
                    var id = parseInt(switches[i].id, 10);
                    if (data.activeSwitches.includes(id)) {
                        switches[i].classList.add("switch-active");
                    } else {
                        switches[i].classList.remove("switch-active");
                    }
                }
            }
        }
    };
    xhr.onerror = function () {
        console.error('Error fetching meter reading');
    };
    xhr.send();
}

setInterval(updatePage, 500); // Update every 500 ms
window.onload = updatePage; // Initial load
