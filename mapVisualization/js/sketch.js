mapHeights = [];
mapSize = 0;
CELL_SIZE = 30;
HEIGHT_SCALAR = 5;

COLORS = 
[
    "#0000FF", // Water
    "#03fcdb", // Shore
    "#ffce54", // Beach
    "#bbff54", // Grassy Beach
    "#00b803", // Grassy Knoll
    "#7507e3", // Hilly Area
    "#6f5c82", // Rocky Outcropping
    "#a6a7f7", // Mountain Side
    "#a1a1a1", // Mountain Top
    "#f0fcff", // Clouds
];
var c;
function setup() {
    //c = createCanvas(window.innerWidth * .99, window.innerHeight * .8, WEBGL);
    height = 1080
    c = createCanvas(height * 1.7,height, WEBGL);
}
  
var HAS_SAVE = false;
function draw() {
    orbitControl();
    background(100);

    translate((-mapSize * .68) * CELL_SIZE,0,-700)

    rotateX(-PI/6)
    rotateY(PI/3)
    for(var x = 0; x < mapSize; x++)
    {
        push();
        for(var y = 0; y < mapSize; y++)
        {
            push();
            var curCellHeight = mapHeights[x][y]
            if(x == 0 && y == 0)
            {
                fill("#ff0000");
            }
            else
            {
                colorStr = COLORS[int(curCellHeight)]
                fill(colorStr)
            }

            stroke(1)
            var boxHeight = curCellHeight * HEIGHT_SCALAR;
            translate(x * CELL_SIZE,boxHeight * -.5,y * CELL_SIZE);
            box(CELL_SIZE, boxHeight, CELL_SIZE);
            pop();
        }
        pop();
    }
    CreateKey();
}

function LoadMap(data)
{
    mapSize = data["heightMap"].length
    mapHeights = data["heightMap"];
    CreateKey();
}

function CreateKey()
{
    var i = 0;
    colorSize = 100;
    for(color of COLORS)
    {
        push();
        fill(color)
        square(0, -500 + i++ * colorSize, colorSize)
        pop();
    }
}

function SaveImage()
{
    saveCanvas(c, 'mapImage', 'png');
}