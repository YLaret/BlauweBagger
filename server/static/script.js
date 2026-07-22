const currentPath = window.location.pathname;

const navlinkoverview = document.querySelector('#nav-link-overview');
const navlinkacc = document.querySelector('#nav-link-acc');
const navlinkcontrol = document.querySelector('#nav-link-control');
const navlinkprogram = document.querySelector('#nav-link-program');
const navlinklog = document.querySelector('#nav-link-log');

if (currentPath == "/")
{
    navlinkoverview.classList.add('active')
    navlinkacc.classList.remove('active')
    navlinkcontrol.classList.remove('active')
    navlinkprogram.classList.remove('active')
    navlinklog.classList.remove('active')
} else if (currentPath == "/acc") {
    navlinkoverview.classList.remove('active')
    navlinkacc.classList.add('active')
    navlinkcontrol.classList.remove('active')
    navlinkprogram.classList.remove('active')
    navlinklog.classList.remove('active')
} else if (currentPath == "/control") {
    navlinkoverview.classList.remove('active')
    navlinkacc.classList.remove('active')
    navlinkcontrol.classList.add('active')
    navlinkprogram.classList.remove('active')
    navlinklog.classList.remove('active')
} else if (currentPath == "/program") {
    navlinkoverview.classList.remove('active')
    navlinkacc.classList.remove('active')
    navlinkcontrol.classList.remove('active')
    navlinkprogram.classList.add('active')
    navlinklog.classList.remove('active')
} else if (currentPath == "/log") {
    navlinkoverview.classList.remove('active')
    navlinkacc.classList.remove('active')
    navlinkcontrol.classList.remove('active')
    navlinkprogram.classList.remove('active')
    navlinklog.classList.add('active')
}

function updatePage() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/updatepage", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            // ACC
            if (currentPath == "/acc") {

                data.controls.forEach(function(control) {

                    var chart = charts[control.ControlID];

                    if (chart) {
                        chart.data.labels = control.time;

                        chart.data.datasets[0].data = control.meas;
                        chart.data.datasets[1].data = control.ref;
                        chart.data.datasets[2].data = control.freq;

                        chart.update();
                    }

                });
            }
            
            // HMI VIEW
            if (currentPath == "/") {
                // hmi update state
                var switches = document.getElementsByClassName("hmi-pump");
                if (data.activeSwitches) {
                    for (var i = 0; i < switches.length; i++) {
                        var id = parseInt(switches[i].id, 10);
                        if (data.activeSwitches.includes(id)) {
                            switches[i].classList.add("hmi-active");
                        } else {
                            switches[i].classList.remove("hmi-active");
                        }
                    }
                }
                
                // controls update state
                var auto = document.getElementById("auto-btn");
                if (data.pause == 14) {
                    auto.classList.add("auto-active");
                } else {
                    auto.classList.remove("auto-active");
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
                
                document.getElementById("hmi-mix").innerText = data.aM.mix;
                mix = document.getElementById("hmi-mix-container");
                if (data.aM.mix == "OK") {
                    mix.classList.add("hmi-lvl-ok");
                } else {
                    mix.classList.remove("hmi-lvl-ok");
                }
                document.getElementById("hmi-vuil").innerText=data.aM.vuil;
                vuil = document.getElementById("hmi-vuil-container");
                if (data.aM.vuil == "OK") {
                    vuil.classList.add("hmi-lvl-ok");
                } else {
                    vuil.classList.remove("hmi-lvl-ok");
                }
                document.getElementById("hmi-schoon").innerText=data.aM.schoon;
                schoon = document.getElementById("hmi-schoon-container");
                if (data.aM.schoon == "OK") {
                    schoon.classList.add("hmi-lvl-ok");
                } else {
                    schoon.classList.remove("hmi-lvl-ok");
                }
                document.getElementById("hmi-pers").innerText=data.meters[2];
                /*
                schoon = document.getElementById("hmi-pers-container");
                if (data.aM.pers == "OK") {
                    schoon.classList.add("hmi-lvl-ok");
                } else {
                    schoon.classList.remove("hmi-lvl-ok");
                }
                */
                document.getElementById("hmi-0").innerText = data.meters[0];
                document.getElementById("hmi-1").innerText = data.meters[1];
                document.getElementById("hmi-2").innerText = "-";
                document.getElementById("hmi-3").innerText = "-";
            }
            // CONTROL VIEW
            if (currentPath == "/control") {
                var start = document.getElementById("start-btn");
                if (data.pause == 0) {
                    start.classList.add("start-active");
                } else {
                    start.classList.remove("start-active");
                }
                // controls update state
                var auto = document.getElementById("auto-btn");
                if (data.pause == 14) {
                    auto.classList.add("auto-active");
                } else {
                    auto.classList.remove("auto-active");
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
