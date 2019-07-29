mapHeights = [];
mapSize = 0;
CELL_SIZE = 20;
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

let VIEWS = {
    "corner": "corner",
    "side": "side",
    "top": "top"
};
let VIEW = VIEWS.corner;
var c;
function setup() {
    height = 4080;
    frameRate(20);
    p5.disableFriendlyErrors = true; // disables Friendly errors

    CreateViewSwitcher();
    c = createCanvas(height * 1.7,height, WEBGL);
}

  
var HAS_SAVE = false;
function draw() {
    orbitControl();
    background("#070d17");
    push();            


    switch(VIEW)
    {
        case VIEWS.corner:

            translate((-mapSize * .50) * CELL_SIZE,(-mapSize * .25) * CELL_SIZE,1000)
            rotateX(-PI/6)
            rotateY(PI/3)
            translate((-mapSize * .55) * CELL_SIZE,0,200)

            break;
        case VIEWS.top:
            rotateX(-PI/2);
            translate((-mapSize * .50) * CELL_SIZE,-1900,(-mapSize * .50) * CELL_SIZE)
            break;
        case VIEWS.side:
            translate((-mapSize * .50) * CELL_SIZE,(-mapSize * .25) * CELL_SIZE,1000)
            rotateX(-PI/6)
            break;
        
    }

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
            strokeWeight(1)
            var boxHeight = curCellHeight * HEIGHT_SCALAR;
            translate(x * CELL_SIZE,boxHeight * -.5,y * CELL_SIZE);
            box(CELL_SIZE, boxHeight, CELL_SIZE);
            pop();
        }
        pop();
    }
    CreateKey();
    pop();
}

function LoadMap(data)
{
    clear();
    mapSize = data["heightMap"].length;
    mapHeights = data["heightMap"];

    // This ensures the map always fills the viewing window
    CELL_SIZE = 1800 / mapSize;
    HEIGHT_SCALAR = CELL_SIZE * .25;
    CreateKey();
}

function CreateKey()
{
    var i = 0;
    colorSize = 100;
    for(color of COLORS)
    {
        push();
        rotateZ(PI/9);     
        rotateX(PI);
        fill(color)
        square(-200, -500 + i++ * colorSize, colorSize)
        pop();
    }
}

function CreateViewSwitcher()
{
    for(view in VIEWS)
    {
        newBtn = document.createElement("input");
        newBtn.type = "button";
        newBtn.value = VIEWS[view]

        document.getElementById("views").appendChild(newBtn);
        newBtn.addEventListener("click", function(e)
        {
            VIEW = e.target.value;
        });
    }
}

function SaveImage()
{
    saveCanvas(c, 'mapImage', 'png');
}