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
        else if(location == "University Recreation Center 120"){
            largeImage.src = '../img/rec.jpg'; 
            largeImage.style.display = 'block';
        }
        else if(location == "Anderson Hall 370"){
            largeImage.src = '../img/anderson.jpg'; 
            largeImage.style.display = 'block';
        }
        else if(location == "Folwel Hall 12"){
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