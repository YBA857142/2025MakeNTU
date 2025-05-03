// Same brown filter and ellipse detection logic
function brownFilter(img) {
  const hsv = img.cvtColor(cv.COLOR_BGR2HSV);
  const lowerBrown = new cv.Vec(5, 0, 0);
  const upperBrown = new cv.Vec(70, 255, 60);
  return hsv.inRange(lowerBrown, upperBrown);
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
  return largestEllipse;
}

module.exports = { findEllipse };
