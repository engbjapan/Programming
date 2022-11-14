let cv;

let last_mouseX=80;
let last_mouseY=80;
let width_=80
let SCrollUP_=1

function setup() {
  cv=createCanvas(400, 400);
  cv.mouseWheel((event) =>{
    if (event.deltaY >= SCrollUP_) {
      if (width_ <cv.elt.width/2) width_+=10;
    }else {
      if (width_ > 10) width_ -= 10;
    }});
}

function draw() {
  background(220);
  if (mouseIsPressed){
    last_mouseX=mouseX;last_mouseY = mouseY;
    circle(mouseX,mouseY,width_);
  }else{  
    circle(last_mouseX,last_mouseY,width_);
  }
}
