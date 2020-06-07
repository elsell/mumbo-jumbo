playerPos = []
mapHeights = [];
mapTrees = []
mapRivers = []
mapEnemies = []
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
    "#a1a1aF", // Mountain Top
    "#f0fcff", // Clouds
];
FOLIAGE_COLORS = 
[
    "#bdb76b", 
    "#8fbc8f", 
    "#556b2f", 
    "#006400", 
    "#228b22",
    "#696969",  
    "#755c0f", 
    "#008000", 
    "#fffacd", 
    "#f0e68c", 
];

let VIEWS = {
    "corner": "corner",
    "side": "side",
    "top": "top"
};
let VIEW = 22;//VIEWS.corner;
var c;
function setup() {
    height = 3500;
    width = height * 1.77;
    frameRate(20);
    p5.disableFriendlyErrors = true; // disables Friendly errors, apparently more performant

    CreateViewSwitcher();
    c = createCanvas(width,height, WEBGL);
    debugMode(5000, 100, 0, 0, 0, 2000, 0, -1000, 0);
}

  
var HAS_SAVE = false;
function draw() {
    orbitControl();
    background("#e0e0e0");
    push();            
    
    rotateY(PI/2);
    translate((-mapSize * .50) * CELL_SIZE,0,(-mapSize * .50) * CELL_SIZE)
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
            var curCellHeight = mapHeights[x][y];
            if(x == 0 && y == 0)
            {
                fill("#ff0000");
            }
            else
            {
                colorStr = COLORS[int(curCellHeight)];
                fill(colorStr);
            }

            // Draw Terrain
            stroke("#0e0e0e");
            strokeWeight(1);
            var boxHeight = curCellHeight * HEIGHT_SCALAR;
            translate(y * CELL_SIZE, boxHeight * -.5,x * CELL_SIZE);
            box(CELL_SIZE, boxHeight, CELL_SIZE);

            // Draw Rivers
            push();
            riverDirection = mapRivers[x][y];
            if(riverDirection > 0)
            {
                fill("#FF0000");
                switch(riverDirection)
                {
                    case 2:
                    case 4:
                        // East/West
                        rotateY(PI/2);
                        break;
                    case 1:
                    case 3:
                        // The box is already oriented North-South
                        break;
                    case 6:
                    case 7:
                        // NE/EN/SW/WS
                        fill("#00ff00")
                        translate(.10 * CELL_SIZE, 0,-.25 * CELL_SIZE);
                        rotateY(-PI/4);
                        break;
                    case 16:
                    case 17:
                        // NE/EN/SW/WS
                        translate(-.10 * CELL_SIZE, 0,.25 * CELL_SIZE);
                        fill("#aaff00")
                        rotateY(-PI/4);
                        
                        break;
                    case 5:
                    case 8:
                        // NW/WN/SE/ES
                        fill("#0000ff")
                        rotateY(PI/4);
                        translate(.10 * CELL_SIZE, 0,.25 * CELL_SIZE);
                        break;
                    case 15:
                    case 18:
                        translate(-.10 * CELL_SIZE, 0,-.25 * CELL_SIZE);
                        fill("#00aaff")
                        rotateY(PI/4);
                        break;
                    case 9:
                        // A puddle :P
                        scale(.5,1,2.5);
                        fill("#FF0000")
                        break;
                    case 10:
                        // A river mouth ;D
                        scale(.5,1,2.5);
                        fill("#FF44AA");
                        break;
                    case 11:
                        // A swamp!
                        scale(.5,1,2.5);
                        fill("#5a6b16");
                        break;                        

                }
                box(CELL_SIZE + 1, boxHeight + 1 , CELL_SIZE * .2 + 1);
            }
            pop();
            // Draw Trees
            push();
            var numTrees = int(mapTrees[x][y]);
            if(numTrees > 0) 
            {
                var treeHeight = CELL_SIZE * numTrees * .7
                translate(0,-boxHeight * .5 - treeHeight * .5 ,0);
                translate(0,0,0);
    
                colorStr = FOLIAGE_COLORS[int(numTrees)];
                fill(colorStr);
                box(CELL_SIZE * .25,  treeHeight,CELL_SIZE * .25);
            }
            pop();

            // Draw enemies
            push();
            var curEnemy = mapEnemies[x][y];
            if(curEnemy !== null)
            {
                var treeHeight = CELL_SIZE * 15
                translate(0,-boxHeight * .5 - treeHeight * .5 ,0);
                translate(0,0,0);
                
                fill("#FF0000");
                box(CELL_SIZE * .15,  treeHeight,CELL_SIZE * .15);
            }
            pop();

            // Draw Player Pos
            push();

            try
            {
                if(playerPos.x  == x && playerPos.y  == y)
                {
                    var treeHeight = CELL_SIZE * 15
                    translate(0,-boxHeight * .5 - treeHeight * .5 ,0);
                    fill("#00FFFF");
                    box(CELL_SIZE * .15,  treeHeight,CELL_SIZE * .15);
                }
            }catch(e)
            {
                //console.error(e);
            }
            
            
            pop();
            pop();
        }
        pop();
    }
    pop();
    CreateKey();
    pop();
}

function LoadMap(data)
{
    clear();
    mapSize = data["heightMap"].length;
    mapHeights = data["heightMap"];
    mapTrees = data["treeMap"];
    mapRivers = data["riverMap"];
    mapEnemies = data["enemyMap"]
    playerPos = data["playerPosition"]

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
    save(c, 'mapImage.png');
}