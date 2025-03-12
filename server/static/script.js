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

function updatePage() {
            fetch('/updatepage')
                .then(response => response.json())
                .then(data => {
                    console.log(data.activeSwitches);
                    console.log(data.meters);
                    console.log(data.programRunTime);
                    document.getElementById("program-run-time").innerText = data.programRunTime
                    const meters = document.getElementsByClassName("meters");
                    for (let i = 0; i < meters.length; i++) {
                        meters.item(i).innerText = data.meters[i];
                    }
                    const switches = document.getElementsByClassName("switches")
                    for (let i = 0; i < switches.length; ++) {
                        const id = parseInt(switches.item(i).id)
                        if data.activeSwitches.includes(id) {
                            switches.item(i).add("switch-active")
                        } else {
                            switches.item(i).remove("switch-active")
                        }
                    }
                    /*let meter = document.getElementById("meter");
                    meter.value = data.reading;
                    document.getElementById("meter_value").innerText = data.reading;*/
                })
                .catch(error => console.error('Error fetching meter reading:', error));
        }

setInterval(updatePage, 200); // Update every 2 seconds
window.onload = updatePage; // Initial load
