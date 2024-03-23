document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('.schedule-table tr');

    rows.forEach((row, index) => {
        row.addEventListener('mouseover', () => showImage(row));
        row.addEventListener('mouseout', () => hideImage());
    });

    function showImage(row) {
        const largeImage = document.querySelector('#large-image');
        const location = row.cells[3].textContent.trim(); 
        if(location=="Remote Class"){
            largeImage.src = '../img/zoom.jpg'; 
            largeImage.style.display = 'block';    
        }
        else if(location == "123 SE Harvard St, Minneapolis, MN 55455 Recwell Center room 120"){
            largeImage.src = '../img/rec.jpg'; 
            largeImage.style.display = 'block';
        }
        else if(location == "257 S 19th Ave, Minneapolis, MN 55455 Anderson Hall room 370"){
            largeImage.src = '../img/anderson.jpg'; 
            largeImage.style.display = 'block';
        }
        else if(location == "9 Pleasant St SE, Minneapolis, MN 55455 Folwel Hall room 103"){
            largeImage.src = '../img/folwel.jpg'; 
            largeImage.style.display = 'block';
        }
        else if(location=="Event Location (Virtual or Physical)"){
            largeImage.src = '../img/gophers-mascot.png'; 
            largeImage.style.display = 'block';
        }
    }

    function hideImage() {
        const largeImage = document.querySelector('#large-image');
        largeImage.style.display = 'block';
    }
});