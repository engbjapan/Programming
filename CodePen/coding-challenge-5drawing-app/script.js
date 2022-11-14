/*** GUI Part ***/
var tool = 0;
var tools = document.querySelectorAll(".tool");
var drawColor = null;
//var radius = 20;

var toolsmouse = 0;
setColor([50, 50, 60]);

for (var i = 0; i < tools.length; i++) {
  tools[i].onclick = (function (id) {
    return function () {
      setTool(id);
    };
  })(i);
}

function setTool(id) {
  tool = id;
  for (var i = 0; i < tools.length; i++) {
    tools[i].classList.remove("tool-selected");
    if (id == i) tools[i].classList.add("tool-selected");
  }
}

function setColor(c) {
  drawColor = c;
}
var radiusel_ = document.querySelector("#radius-range");
var toolsel_ = document.querySelector("#tools");
document.onwheel = function (e) {
  if (e.deltaY < 0) radiusel_.value = parseInt(radiusel_.value) + 2;
  else radiusel_.value = parseInt(radiusel_.value) - 2;
};
toolsel_.onmouseover = () => {
  toolsmouse = 1;
};
toolsel_.onmouseout = () => {
  toolsmouse = 0;
};

document.querySelector("#download").onclick = () => {
  graphic.save("Drawing.png");
};
radiusel_.oninput = (e) => {
  radiusel_.value = parseInt(e.target.value);
};
document.querySelector("#colorPicker").oninput = (e) => {
  setColor(e.target.value);
};

/*** Drawing part ***/
var lastPoint = null;
var graphic = null;

var squareOrigin = null;
var circleOrigin = null;
let colorPicker;
function setup() {
  createCanvas(
    document.body.clientWidth,
    document.body.clientHeight - 50
  ).parent("#canvas");
  ellipseMode(CENTER);
  graphic = createGraphics(
    document.body.clientWidth,
    document.body.clientHeight - 50
  );
  graphic.background(255);
}
var radius;
function draw() {
  background(255);
  image(graphic, 0, 0);
  radius = parseInt(radiusel_.value);
  if ((tool == 0 || tool == 3) && toolsmouse == 0) tool0Preview();

  if (mouseIsPressed && toolsmouse == 0) {
    drawOnGraphic();
  } else {
    lastPoint = null;
    onMouseQuit();
  }
}

function tool0Preview() {
  noFill();
  stroke(200);
  strokeWeight(2);
  ellipse(mouseX, mouseY, radius, radius);
}

function drawOnGraphic() {
  if (lastPoint == null) lastPoint = [mouseX, mouseY];

  if (tool == 0) {
    graphic.noFill();
    graphic.stroke(drawColor);
    graphic.strokeWeight(radius);
    graphic.line(mouseX, mouseY, lastPoint[0], lastPoint[1]);
  }

  if (tool == 1) {
    if (squareOrigin == null) {
      squareOrigin = [mouseX, mouseY];
    } else {
      fill([0, 0, 0, 122]);
      noStroke();
      rect(
        squareOrigin[0],
        squareOrigin[1],
        mouseX - squareOrigin[0],
        mouseY - squareOrigin[1]
      );
    }
  }
  if (tool == 2) {
    if (circleOrigin == null) {
      circleOrigin = [mouseX, mouseY];
    } else {
      fill([0, 0, 0, 122]);
      noStroke();
      let d = createVector(
        mouseX - circleOrigin[0],
        mouseY - circleOrigin[1]
      ).mag();
      ellipseMode(CENTER);
      ellipse(circleOrigin[0], circleOrigin[1], d * 2, d * 2);
    }
  }

  if (tool == 3) {
    graphic.noFill();
    graphic.stroke(255);
    graphic.strokeWeight(radiusel_.value);
    graphic.line(mouseX, mouseY, lastPoint[0], lastPoint[1]);
  }

  lastPoint = [mouseX, mouseY];
}

function onMouseQuit() {
  if (squareOrigin != null) {
    graphic.fill(drawColor);
    graphic.noStroke();
    graphic.rect(
      squareOrigin[0],
      squareOrigin[1],
      mouseX - squareOrigin[0],
      mouseY - squareOrigin[1]
    );
    squareOrigin = null;
  }
  if (circleOrigin != null) {
    graphic.fill(drawColor);
    graphic.noStroke();
    let d = createVector(
      mouseX - circleOrigin[0],
      mouseY - circleOrigin[1]
    ).mag();
    graphic.ellipseMode(CENTER);
    graphic.ellipse(circleOrigin[0], circleOrigin[1], d * 2, d * 2);
    circleOrigin = null;
  }
}