// RandomPicture.js
// User-triggered (Manual) Random image selection using arrays
var iconImg; 
var pictures = [ "CPE", "EPT", "GPP", "GUI", "PERF", "PORT", "SEO" ];
var descriptions = [ "Common Programming Error", 
   "Error-Prevention Tip", "Good Programming Practice", 
   "Look-and-Feel Observation", "Performance Tip", "Portability Tip", 
   "Software Engineering Observation" ];

// every time
// a user clicks on the image
// pick a random image and corresponding description then modify
// the img element in the document's body 
function pickImage()
{
   var index = Math.floor(Math.random() * 7 );
   // console.log("/pngPictires/"+pictures[ index ] + ".png");
   iconImg.setAttribute( "src", "/pngPictures/"+pictures[ index ] + ".png" );
   iconImg.setAttribute( "alt", descriptions[ index ] );
   index = (index+1)%pictures.length;
} // end function pickImage

// registers iconImg's click event handler
// so it adds an event listener to the image displayed by the img tag
// specified in the HTML file
function start()
{
   iconImg = document.getElementById( "image" );
   // iconImg.addEventListener( "click", pickImage, false );
   var int =  setInterval("pickImage()",1000);   
} // end function start

// on the window load event,call the start function
// window.addEventListener( "load", start, false );

