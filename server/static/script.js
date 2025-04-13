const currentPath = window.location.pathname;

const navlinkoverview = document.querySelector('#nav-link-overview');
const navlinktableview = document.querySelector('#nav-link-tableview');
const navlinkprogram = document.querySelector('#nav-link-program');

if (currentPath == "/")
{
    navlinkoverview.classList.add('active')
    navlinktableview.classList.remove('active')
    navlinkprogram.classList.remove('active')
} else if (currentPath == "/log") {
    navlinkoverview.classList.remove('active')
    navlinktableview.classList.add('active')
    navlinkprogram.classList.remove('active')
} else if (currentPath == "/program") {
    navlinkoverview.classList.remove('active')
    navlinktableview.classList.remove('active')
    navlinkprogram.classList.add('active')
}

function updatePage() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/updatepage", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            
            // meters update state
            var meters = document.getElementsByClassName("meters");
            for (var i = 0; i < meters.length; i++) {
                meters[i].innerText = data.meters[i];
            }
            
            // program stage update
            document.getElementById("program-name").innerText = data.programName;
            document.getElementById("stage-name").innerText = data.stageName;
            document.getElementById("next-stage-name").innerText = data.nextStageName;
            document.getElementById("program-run-time").innerText = data.programRunTime;
            document.getElementById("total-program-time").innerText = data.totalProgramTime;
            document.getElementById("stage-run-time").innerText = data.stageRunTime;
            document.getElementById("total-stage-time").innerText = data.totalStageTime;
            var progress = document.getElementById("program-progress");
            progress.value = data.programRunTime;
            progress.max = data.totalProgramTime
            
            // switches update state
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
            
            // controls update state
            var start = document.getElementById("start-btn");
            if (data.pause == 0) {
                start.classList.add("start-active");
            } else {
                start.classList.remove("start-active");
            }
            var pause = document.getElementById("pause-btn");
            if (data.pause == 1) {
                pause.classList.add("pause-active");
            } else {
                pause.classList.remove("pause-active");
            }
            var stop = document.getElementById("stop-btn");
            if (data.pause == 2) {
                stop.classList.add("stop-active");
            } else {
                stop.classList.remove("stop-active");
            }
        }
    };
    xhr.onerror = function () {
        console.error('Error fetching CMS reading');
    };
    xhr.send();
}

setInterval(updatePage, 500); // Update every 500 ms
window.onload = updatePage; // Initial load
