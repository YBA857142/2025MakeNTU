// Same brown filter and ellipse detection logic
function brownFilter(canvasId) {
    const img = cv.imread(canvasId);  // get OpenCV Mat from canvas
    const hsv = new cv.Mat();
    cv.cvtColor(img, hsv, cv.COLOR_RGB2HSV);
  
    const lowerBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [5, 0, 0, 0]);
    const upperBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [70, 255, 60, 255]);
  
    const mask = new cv.Mat();
    cv.inRange(hsv, lowerBrown, upperBrown, mask);
  
    // Clean up
    img.delete();
    hsv.delete();
    lowerBrown.delete();
    upperBrown.delete();
  
    return mask;
  }
  
  function findEllipse(img) {
    const brownMask = brownFilter(img);
    const blurred = brownMask.gaussianBlur(new cv.Size(5, 5), 0);
    const edges = blurred.canny(50, 150);
  
    const contours = edges.findContours(cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
    let largestEllipse = null;
    let maxArea = 0;
  
    for (let contour of contours) {
      if (contour.numPoints >= 5) {
        const ellipse = contour.fitEllipse();
        const area = Math.PI * (ellipse.axes.width / 2) * (ellipse.axes.height / 2);
        if (area > maxArea) {
          maxArea = area;
          largestEllipse = ellipse;
        }
      }
    }
  
    // if (largestEllipse) {
      // img.drawEllipse(largestEllipse, new cv.Vec(0, 255, 0), 2, cv.LINE_8);
    // }
  
    // return img;
    console.log(largestEllipse);
    return largestEllipse;
  }

// Config Variables
const intervalSeconds = 1; // seconds

// Main function
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const intervalInput = document.getElementById('interval');
    const toggleBtn = document.getElementById('toggleBtn');
    const statusDiv = document.getElementById('status');
    
    let captureInterval;
    let stream;
    
    // Setup canvas context
    const context = canvas.getContext('2d');
    
    toggleBtn.isOn = false;
    function toggleButtonText(){
        toggleBtn.isOn = !toggleBtn.isOn;
        toggleBtn.innerHTML = toggleBtn.isOn ? "Stop Capture" : "Start Capture";
        return toggleBtn.isOn;
    }
    
    // Start the camera
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            video.srcObject = stream;
            
            // Set canvas dimensions once we have video dimensions
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            };
            
            showStatus('Camera started successfully', 'success');
        } catch (err) {
            showStatus(`Error accessing camera: ${err.message}`, 'error');
            console.error('Error accessing camera:', err);
        }
    }
    
    // Stop the camera
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            video.srcObject = null;
        }
    }
    
    // Capture image from video
    function captureImage() {
        // Draw current video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        let ellipse = findEllipse(canvas);
        if (ellipse) {
            // Draw ellipse on canvas
            context.beginPath();
            context.ellipse(ellipse.center.x, ellipse.center.y, ellipse.axes.width / 2, ellipse.axes.height / 2, 0, 0, 2 * Math.PI);
            context.strokeStyle = 'red';
            context.lineWidth = 2;
            context.stroke();
        }
        
        // Convert canvas to image data URL
        const imageDataUrl = canvas.toDataURL('image/jpeg', 0.8);
        
        // Update the captured image preview
        // capturedImage.src = imageDataUrl;
        
        // Send the image to the server
        sendImageToServer(imageDataUrl);
        
        return imageDataUrl;
    }
    
    // Send image to server
    async function sendImageToServer(imageDataUrl) {
        try {
            // Remove the data:image/jpeg;base64, prefix to get just the base64 data
            const base64Data = imageDataUrl.split(',')[1];
            
            const response = await fetch('/api/image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    timestamp: new Date().toISOString(),
                    imageData: base64Data
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                showStatus(`Image sent successfully at ${new Date().toLocaleTimeString()}`, 'success');
            } else {
                showStatus(`Error sending image: ${response.statusText}`, 'error');
            }
        } catch (err) {
            showStatus(`Error sending image: ${err.message}`, 'error');
            console.error('Error sending image:', err);
        }
    }
    
    // Display status message
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = type;
        
        // Clear the status after 5 seconds
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = '';
        }, 5000);
    }
    
    // Start periodic capture
    function startCapture() {
        
        // Initial capture
        captureImage();
        
        // Schedule periodic captures
        captureInterval = setInterval(captureImage, intervalSeconds * 1000);
        
        intervalInput.disabled = true;
        
        showStatus(`Capture started with ${intervalSeconds} second interval`, 'success');
    }
    
    // Stop periodic capture
    function stopCapture() {
        clearInterval(captureInterval);

        intervalInput.disabled = false;
        
        showStatus('Capture stopped', 'success');
    }
    
    // Event listeners
    toggleBtn.addEventListener('click', () => {
        toggleButtonText();
        if (toggleBtn.isOn){
            startCamera().then(() => {
                // Wait a bit for camera to initialize before starting capture
                setTimeout(startCapture, 1000);
            });
        } else {
            stopCapture();
            stopCamera();
        }
    });
    
    // Clean up resources when page is closed
    window.addEventListener('beforeunload', () => {
        stopCapture();
        stopCamera();
    });
});