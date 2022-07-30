const HOURHAND = document.querySelector("#hour");
const MINUTEHAND = document.querySelector("#minute");
const SECONDHAND = document.querySelector("#second");

const SCHEDULE = document.querySelector("#schedule");

async function runTheClock() {
    fetch('http://127.0.0.1:5000/get_data')
        .then((response) => response.json())
        .then((data) => {
            turnHands(new Date(data.time), data.show_seconds);
            updateSchedule(data.schedule);
        })
}

function updateSchedule(schedule) {
    var ul = document.createElement('ul');
    ul.setAttribute('class','schedule_list');

    schedule.forEach((task) =>{
        var time_text = task[0]
        var text = task[1]
        var is_current = task[2]

        var li = document.createElement('li');
        li.innerHTML = '<em>' + time_text + '</em> ' + text;
        ul.appendChild(li);

        if (is_current) {
            li.setAttribute('class','current');
        }
    })

    SCHEDULE.innerHTML = ul.outerHTML;
}

function turnHands(date, show_seconds) {

    if (show_seconds) {
        SECONDHAND.style.display = "block";
    } else {
        SECONDHAND.style.display = "none";
    }

    let hr = date.getHours();
    let min = date.getMinutes();
    let sec = date.getSeconds();    

    let hrPosition = (hr*360/12) + (min*(360/60)/12);
    let minPosition = (min*360/60) + (sec*(360/60)/60);
    let secPosition = sec*360/60;

    hrPosition = hrPosition + (3/360);
    minPosition = minPosition + (6/60);
    secPosition = secPosition + 6;

    HOURHAND.style.transform = "rotate(" + hrPosition + "deg)";
    MINUTEHAND.style.transform = "rotate(" + minPosition + "deg)";
    SECONDHAND.style.transform = "rotate(" + secPosition + "deg)";
    
}


var interval = setInterval(runTheClock, 100);