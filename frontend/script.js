// Config Variables
const intervalSeconds = 0.05; // seconds

// Update the toggle button event listener to call the modified startCamera function:
toggleBtn.addEventListener('click', () => {
    toggleButtonText();
    if (toggleBtn.isOn){
        startCamera().then(() => { // Call the modified startCamera function
            // Wait a bit for camera to initialize before starting capture
            setTimeout(startCapture, 1000);
        });
    } else {
        stopCapture();
        stopCamera();
    }
});

// Same brown filter and ellipse detection logic
function brownFilter(canvasId) {
    const img = cv.imread(canvasId);  // get OpenCV Mat from canvas
    const hsv = new cv.Mat();
    cv.cvtColor(img, hsv, cv.COLOR_RGB2HSV);
  
    const lowerBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [5, 0, 0, 0]);
    const upperBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [70, 255, 100, 255]);
  
    const mask = new cv.Mat();
    cv.inRange(hsv, lowerBrown, upperBrown, mask);
  
    // Clean up
    img.delete();
    hsv.delete();
    lowerBrown.delete();
    upperBrown.delete();
  
    return mask;
}

function findEllipse(canvasId) {
    const brownMask = brownFilter(canvasId);
    const blurred = new cv.Mat();
    cv.GaussianBlur(brownMask, blurred, new cv.Size(5, 5), 0);
    const edges = new cv.Mat();
    cv.Canny(blurred, edges, 50, 150);
  
    const contours = new cv.MatVector();
    const hierarchy = new cv.Mat();
    cv.findContours(edges, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
  
    let largestEllipse = null;
    let maxArea = 0;
  
    for (let i = 0; i < contours.size(); ++i) {
        const contour = contours.get(i);
        if (contour.data32S.length / 2 >= 5) { // Ensure at least 5 points for fitEllipse
            const rotatedRect = cv.fitEllipse(contour);
            const ellipse = {
            center: rotatedRect.center,
            axes: rotatedRect.size,
            angle: rotatedRect.angle
            };
            const area = Math.PI * (ellipse.axes.width / 2) * (ellipse.axes.height / 2);
            const lowerMax = Math.floor(canvas.height * 3 / 10);
            const upperMax = Math.floor(canvas.height * 9 / 10);
            if (area > 800) {
                if (ellipse.axes.width > 70 | ellipse.axes.height > 70) {
                    continue;
                }
                if (ellipse.center.y < lowerMax) {
                    continue;
                }
                if (ellipse.center.y > upperMax) {
                    continue;
                }
                const threshold = 2000 * (ellipse.center.y - lowerMax) / (upperMax - lowerMax) + 1000;
                if (area > threshold) {
                    continue;
                }
                if (area > maxArea) {
                    maxArea = area;
                    largestEllipse = ellipse;
                }
            }
            contour.delete();
        }
    }
  
    brownMask.delete();
    blurred.delete();
    edges.delete();
    contours.delete();
    hierarchy.delete();
  
    console.log(largestEllipse);
    return largestEllipse;
}// Same brown filter and ellipse detection logic
function brownFilter(canvasId) {
    const img = cv.imread(canvasId);  // get OpenCV Mat from canvas
    const hsv = new cv.Mat();
    cv.cvtColor(img, hsv, cv.COLOR_RGB2HSV);
  
    const lowerBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [5, 0, 0, 0]);
    const upperBrown = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [70, 255, 100, 255]);
  
    const mask = new cv.Mat();
    cv.inRange(hsv, lowerBrown, upperBrown, mask);
  
    // Clean up
    img.delete();
    hsv.delete();
    lowerBrown.delete();
    upperBrown.delete();
  
    return mask;
}

function findEllipse(canvasId) {
    const brownMask = brownFilter(canvasId);
    const blurred = new cv.Mat();
    cv.GaussianBlur(brownMask, blurred, new cv.Size(5, 5), 0);
    const edges = new cv.Mat();
    cv.Canny(blurred, edges, 50, 150);
  
    const contours = new cv.MatVector();
    const hierarchy = new cv.Mat();
    cv.findContours(edges, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
  
    let largestEllipse = null;
    let maxArea = 0;
  
    for (let i = 0; i < contours.size(); ++i) {
        const contour = contours.get(i);
        if (contour.data32S.length / 2 >= 5) { // Ensure at least 5 points for fitEllipse
            const rotatedRect = cv.fitEllipse(contour);
            const ellipse = {
            center: rotatedRect.center,
            axes: rotatedRect.size,
            angle: rotatedRect.angle
            };
            const area = Math.PI * (ellipse.axes.width / 2) * (ellipse.axes.height / 2);
            const lowerMax = Math.floor(canvas.height * 3 / 10);
            const upperMax = Math.floor(canvas.height * 18.5 / 20);
            if (area > 200) {
                if (ellipse.axes.width > 45 | ellipse.axes.height > 45) {
                    continue;
                }
                if (ellipse.center.y < lowerMax) {
                    continue;
                }
                if (ellipse.center.y > upperMax) {
                    continue;
                }
                const threshold = 1500 * (ellipse.center.y - lowerMax) / (upperMax - lowerMax) + 800;
                if (area > threshold) {
                    continue;
                }
                if (area > maxArea) {
                    maxArea = area;
                    largestEllipse = ellipse;
                }
            }
            contour.delete();
        }
    }
  
    brownMask.delete();
    blurred.delete();
    edges.delete();
    contours.delete();
    hierarchy.delete();
  
    console.log(largestEllipse);
    return largestEllipse;
}

function wait50Milliseconds() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {resolve(true)}, 50);
    })
}

function coordinateConversion(x, y, maxX, maxY) {
    return [Math.floor(x - maxX / 2) + 1, Math.max(maxY - y - 120, 0) + 1];
}

function findColor(canvas, context) {
    let imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    let data = imageData.data;
    let totalRed = 0;
    let totalGreen = 0;
    let totalBlue = 0;
    let count = 0;
    for (let i = 0; i < data.length; i += 4) {
        totalRed += data[i];
        totalGreen += data[i + 1];
        totalBlue += data[i + 2];
        count++;
    }

    let averageRed = Math.floor(totalRed / count);
    let averageGreen = Math.floor(totalGreen / count);
    let averageBlue = Math.floor(totalBlue / count);
    return [averageRed, averageGreen, averageBlue];
}

// Main function
document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const toggleBtn = document.getElementById('toggleBtn');
    const statusDiv = document.getElementById('status');
    
    let captureInterval;
    let stream;

    // Wait for OpenCV to be loaded
    let cvIsLoaded = false;
    while (!cvIsLoaded){
        try {
            cv;
            cvIsLoaded = true;
        } catch {
            console.log("Waiting for CV to be loaded...");
            await wait50Milliseconds();
        }
    }
    cv = (cv instanceof Promise) ? await cv : cv;
    
    // Setup canvas context
    const context = canvas.getContext('2d');
    
    toggleBtn.isOn = false;
    toggleBtn.classList.add("buttonOff");
    function toggleButtonText(){
        toggleBtn.isOn = !toggleBtn.isOn;
        toggleBtn.innerHTML = toggleBtn.isOn ? "Stop Capture" : "Start Capture";
        if (toggleBtn.isOn){
            toggleBtn.classList.add("buttonOn");
            toggleBtn.classList.remove("buttonOff");
        } else {
            toggleBtn.classList.add("buttonOff");
            toggleBtn.classList.remove("buttonOn");
        }
        return toggleBtn.isOn;
    }
    
    // Start the camera
    async function startCamera() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
    
            if (videoDevices.length === 0) {
                throw new Error('No video input devices found.');
            }
    
            let selectedDeviceId = null;

            for (let i = videoDevices.length - 1; i >= 0; i--) {
                const device = videoDevices[i];
                selectedDeviceId = device.deviceId;
                if (selectedDeviceId){
                    break;
                }
            }
    
            // If the user didn't confirm any camera, use the first one as fallback
            if (!selectedDeviceId) {
                console.warn('No camera confirmed. Using the first available camera.');
                selectedDeviceId = videoDevices[0].deviceId;
            }
    
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { deviceId: selectedDeviceId }
            });
    
            video.srcObject = stream;
    
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            };
    
            showStatus('Camera started successfully', 'success');
        } catch (err) {
            showStatus(`Error accessing camera: ${err.message}`, 'error');
            alert(`Error accessing camera: ${err.message}`);
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
    async function captureImage() {
        // Draw current video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        let ellipse = findEllipse(canvas);
        let hasCockroach = false;
        let position = [0, 0];
        let color = [0, 0, 0];
        if (ellipse) {
            // Draw ellipse on canvas
            context.beginPath();
            context.ellipse(ellipse.center.x, ellipse.center.y, ellipse.axes.width / 2, ellipse.axes.height / 2, 0, 0, 2 * Math.PI);
            context.strokeStyle = 'red';
            context.lineWidth = 2;
            context.stroke();
            hasCockroach = true
            position = coordinateConversion(ellipse.center.x, ellipse.center.y, canvas.width, canvas.height);
        }
        
        // Send the image to the server
        
        color = findColor(canvas, context);
        await collectPositions(position, color, hasCockroach);
        
        return;
    }

    let prevX = [];
    let prevY = [];
    async function collectPositions(position, color, hasCockroach) {
        if (!hasCockroach) {
            sendPositionToServer(position, color, hasCockroach);
            return;
        }
        prevX.push(position[0]);
        prevY.push(position[1]);
        if (prevX.length >= 3) {
            let prevXUnsorted = [...prevX];
            prevX.sort();
            let xMedian = prevX[1];
            let xIndex = prevXUnsorted.indexOf(prevX[1]);
            let yMedian = prevY[xIndex];
            prevX = [...prevXUnsorted];
            prevX.shift();
            prevY.shift();
            sendPositionToServer([xMedian, yMedian], color, hasCockroach)
        }
    }
    
    // Send position to server
    async function sendPositionToServer(position, color, hasCockroach) {
        try {
            // Remove the data:image/jpeg;base64, prefix to get just the base64 data
                        
            const response = await fetch('/api/position', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    position: position,
                    color: color,
                    has_cockroach: hasCockroach
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                if (!result.is_running){
                    if (toggleBtn.isOn){
                        toggleButtonText();
                    }
                }
                showStatus(hasCockroach ? `Cockroach Position (${position[0]}, ${position[1]}) Sent!` : `No Cockroach!`, 'success');
            } else {
                showStatus(`Error sending data: ${response.statusText}`, 'error');
            }
        } catch (err) {
            showStatus(`Error sending data: ${err.message}`, 'error');
            console.error('Error sending data:', err);
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

        // fetch('/api/run', {
        //     method: "POST"
        // });
        
        // Schedule periodic captures
        captureInterval = setInterval(captureImage, intervalSeconds * 1000);
        
        showStatus(`Capture started with ${intervalSeconds} second interval`, 'success');
    }
    
    // Stop periodic capture
    function stopCapture() {
        clearInterval(captureInterval);

        // fetch('/api/stop', {
        //     method: "POST"
        // });
        
        showStatus('Capture stopped', 'success');
    }
    
    
    // Event Listener
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


// async function displayCameras() {
//     try {
//       const devices = await navigator.mediaDevices.enumerateDevices();
//       const cameras = devices.filter(device => device.kind === 'videoinput');
  
//       if (cameras.length > 0) {
//         let cameraList = "Available Cameras:\n";
//         cameras.forEach((camera, index) => {
//           cameraList += `${index + 1}. ${camera.label || `Camera ${index + 1}`}\n`;
//         });
//         alert(cameraList);
//       } else {
//         alert("No cameras found on this device.");
//       }
//     } catch (error) {
//       alert(`Error accessing camera information: ${error}`);
//     }
//   }
  
  // Call the function to display the alert
//   displayCameras();