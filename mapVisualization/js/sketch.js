mapHeights = [];
mapSize = 0;
CELL_SIZE = 30;
HEIGHT_SCALAR = 5;
function setup() {
    createCanvas(window.innerWidth * .99, window.innerHeight * .8, WEBGL);
}
  
function draw() {
    orbitControl();
    background(100);

    rotateX(-PI/6)
    rotateY(PI/4)
    translate(-100,0,0)
    for(var x = 0; x < mapSize; x++)
    {
        push();
        for(var y = 0; y < mapSize; y++)
        {
            push();
            if(x == 0 && y == 0)
            {
                fill("#ff0000");
            }
            else
            {
                var colorStr = "rgb(0," + String(int(mapHeights[x][y] * 25.5)) + "," + String(int(255 - mapHeights[x][y] * 25.5)) + ")";
                fill(colorStr)
            }
            stroke(1)
            var boxHeight = mapHeights[x][y] * HEIGHT_SCALAR;
            translate(x * CELL_SIZE,boxHeight * -.5,y * CELL_SIZE);
            box(CELL_SIZE, boxHeight, CELL_SIZE);
            pop();
        }
        pop();
    }
}

function LoadMap(data)
{
    mapSize = data["heightMap"].length
    mapHeights = data["heightMap"];
}
