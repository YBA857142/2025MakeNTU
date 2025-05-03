document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const capturedImage = document.getElementById('capturedImage');
    const intervalInput = document.getElementById('interval');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusDiv = document.getElementById('status');
    
    let captureInterval;
    let stream;
    
    // Setup canvas context
    const context = canvas.getContext('2d');
    
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
        
        // Convert canvas to image data URL
        const imageDataUrl = canvas.toDataURL('image/jpeg', 0.8);
        
        // Update the captured image preview
        capturedImage.src = imageDataUrl;
        
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
        const intervalSeconds = parseInt(intervalInput.value, 10);
        
        if (isNaN(intervalSeconds) || intervalSeconds < 1) {
            showStatus('Please enter a valid interval (min 1 second)', 'error');
            return;
        }
        
        // Initial capture
        captureImage();
        
        // Schedule periodic captures
        captureInterval = setInterval(captureImage, intervalSeconds * 1000);
        
        // Update UI
        startBtn.disabled = true;
        stopBtn.disabled = false;
        intervalInput.disabled = true;
        
        showStatus(`Capture started with ${intervalSeconds} second interval`, 'success');
    }
    
    // Stop periodic capture
    function stopCapture() {
        clearInterval(captureInterval);
        
        // Update UI
        startBtn.disabled = false;
        stopBtn.disabled = true;
        intervalInput.disabled = false;
        
        showStatus('Capture stopped', 'success');
    }
    
    // Event listeners
    startBtn.addEventListener('click', () => {
        startCamera().then(() => {
            // Wait a bit for camera to initialize before starting capture
            setTimeout(startCapture, 1000);
        });
    });
    
    stopBtn.addEventListener('click', () => {
        stopCapture();
        stopCamera();
    });
    
    // Clean up resources when page is closed
    window.addEventListener('beforeunload', () => {
        stopCapture();
        stopCamera();
    });
});