

var wsuri;
var sessionvar;

if (document.location.origin == "file://") {
    wsuri = "ws://127.0.0.1:8080";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";

}

 var httpUri;

if (document.location.origin == "file://") {
    httpUri = "http://127.0.0.1:8080/lp";

} else {
   httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
               document.location.host + "/lp";
}



// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
    // url: wsuri,
    transports: [
       {
          'type': 'websocket',
          'url': wsuri
       },
       {
          'type': 'longpoll',
          'url': httpUri
       }
    ],
    realm: "realm1"
 });


navigator.getUserMedia = ( navigator.getUserMedia ||
                    navigator.webkitGetUserMedia ||
                    navigator.mozGetUserMedia ||
                    navigator.msGetUserMedia);

var video;
var webcamStream;

const videoConstraints = {
facingMode: 'environment'
};

    function startWebcam() {
    if (navigator.getUserMedia) {
        navigator.getUserMedia (

            // constraints
            {
                video:  videoConstraints, 
                audio: false
            },

            // successCallback
            function(localMediaStream) {
                video = document.querySelector('video');

                video.src = window.URL.createObjectURL(localMediaStream);
                webcamStream = localMediaStream;
            },

            // errorCallback
            function(err) {
                console.log("The following error occured: " + err);
            }
        );
    } else {
        console.log("getUserMedia not supported");
    }  
    }

    function stopWebcam() {
        webcamStream.stop();
    }

    var canvas,canvasTrip, ctx,ctx1;

    function init() {
    // Get the canvas and obtain a context for
    // drawing in it
    canvas = document.getElementById("myCanvas");
    canvasTrip = document.getElementById("myCanvasTrip");
    ctx = canvas.getContext('2d');
    }

    function snapshot() {
        // Draws current image from the video element into the canvas
    ctx.drawImage(video, 0,0, canvas.width, canvas.height);
    console.log("getUserMedia dddd supported");

    dataURL = canvas.toDataURL();
    var strImage = dataURL.split(',')[1];
    sessionvar.publish("com.camera.image",[strImage.toString()]);
    }

    function ProcessedImage (args) {
        canvasTrip = document.getElementById("myCanvasTrip");
        ctx1 = canvasTrip.getContext('2d');
        var image = new Image();
        image.onload = function() {
            ctx1.drawImage(image, 0, 0);
        };
        image.src = 'data:image/jpeg;base64,'+args[0];        
    }
    

    connection.onopen = function (session) {

        console.log("connected");
        sessionvar = session;
        sessionvar.subscribe('com.camera.imagetrip', ProcessedImage).then(
            function (sub) {
                console.log('subscribed to topic');
            },
            function (err) {
               console.log('failed to subscribe to topic', err);
            }
         );
   
     };
     
     connection.open();
     
