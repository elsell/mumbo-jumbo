

playerPos = []
mapHeights = [];
mapTrees = []
mapRivers = []
mapEnemies = []
mapSize = 0;
DRAW_HEIGHTS = true
CELL_SIZE = .01;
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

TREES = []
RIVERS = []
ENEMIES = []
PLAYERS = []

REQUEST_SAVE = false

let VIEWS = {
    "corner": "corner",
    "side": "side",
    "top": "top"
};
let VIEW = 22;//VIEWS.corner;
var c;
var inconsolata;


var camera, scene, renderer, stats;
var geometry, material, mesh;
var controls

init();
animate();
function animate()
{
    controls.update()
    stats.update();
    renderer.render( scene, camera );
    
    if(REQUEST_SAVE)
    {
        REQUEST_SAVE = false;
        dataUrl = renderer.domElement.toDataURL("image/png").replace("image/png", "image/octet-stream");;
        window.location.href = dataUrl
    }

    requestAnimationFrame( animate );
}

function createStats() {
    var stats = new Stats();
    stats.setMode(0);

    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '250';
    stats.domElement.style.left = null;
    stats.domElement.style.right = '20';
    stats.domElement.style.float = "right"

    return stats;
  }

function ResetView()
{

    scene.position.set(0,0,0)
    scene.translateX(CELL_SIZE*mapSize * -.5)
    scene.translateZ(CELL_SIZE*mapSize * .5)

    camera.position.set(
        0,
        mapSize * CELL_SIZE,
        0
    );
    camera.lookAt(new THREE.Vector3
    (
        0,
        0,
        0
    ));
    camera.up.set(0,1,0)

   camera.updateProjectionMatrix();
}

function init() {
    canvases = document.body.getElementsByTagName("canvas");
    if( canvases.length >= 1)
    {
        for(var i = 0; i < canvases.length; i++)
        {
            canvases[i].remove()
        }
    }

    camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10 );
	camera.position.z = 2;
    renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

	scene = new THREE.Scene();
    var alight = new THREE.AmbientLight(0xffffff,.3);
    var light = new THREE.DirectionalLight(0xffffff,.7);
    light.position.x = 0
    light.position.y = 6
    light.position.z = .1

    scene.add(light)
    scene.add(alight)
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true


    stats = createStats()
    document.body.appendChild( stats.domElement );

    setupScene()

}

function ToggleRivers()
{
    for(var i = 0; i < RIVERS.length; i++)
    {
        RIVERS[i].visible = !RIVERS[i].visible;
    }
}

function ToggleTrees()
{
    for(var i = 0; i < TREES.length; i++)
    {
        TREES[i].visible = !TREES[i].visible;
    }
}

function ToggleEnemies()
{
    for(var i = 0; i < ENEMIES.length; i++)
    {
        ENEMIES[i].visible = !ENEMIES[i].visible;
    }
}

function TogglePlayers()
{
    for(var i = 0; i < PLAYERS.length; i++)
    {
        PLAYERS[i].visible = !PLAYERS[i].visible;
    }
}

function GetRiverLength(riverColumn)
{
    length = 0
    for(i = 0; i < riverColumn.length; i++)
    {
        if( riverColumn[i] != 0)
        {
            length++;
        }
    }

    return length
}

var HAS_SAVE = false;
function setupScene() {


    for(var x = 0; x < mapSize; x++)
    {
        for(var y = 0; y < mapSize; y++)
        {
            color = 0;
            var curCellHeight = mapHeights[x][y];
            if(x == 0 && y == 0)
            {
                console.log("OK")
                color = "#ff0000"
            }
            else
            {
                color = COLORS[parseInt(curCellHeight)];
            }

            // Draw Terrain
            var boxHeight = curCellHeight * HEIGHT_SCALAR + .001;
    
            geometry = new THREE.BoxBufferGeometry(CELL_SIZE,boxHeight,CELL_SIZE)
            material = new THREE.MeshPhongMaterial({color:color})
            mesh = new THREE.Mesh(geometry, material)
            mesh.position.x = x * CELL_SIZE
            mesh.position.y = boxHeight * .5
            mesh.position.z = -y * CELL_SIZE
            scene.add(mesh)


            // Draw Rivers
            riverDirection = mapRivers[x][y];
            
            if(riverDirection > 0)
            {
                geometry = new THREE.BoxBufferGeometry(CELL_SIZE * .2,CELL_SIZE*.01,CELL_SIZE)
                material = new THREE.MeshPhongMaterial()
                mesh = new THREE.Mesh(geometry, material)
                mesh.position.x = x * CELL_SIZE 
                mesh.position.y = boxHeight
                mesh.position.z = -y * CELL_SIZE

                color = "#FF0000";
                switch(riverDirection)
                {
                    case 2:
                    case 4:
                        // East/West
                        mesh.rotation.y = Math.PI / 2
                        break;
                    case 1:
                    case 3:
                        // The box is already oriented North-South
                        break;
                    case 6:
                    case 7:
                        // NE/EN/SW/WS
                        color = "#00ff00"
                        mesh.position.x -= .10 * CELL_SIZE
                        mesh.position.z += -.25 * CELL_SIZE;
                        mesh.rotation.y = -Math.PI/4
                        break;
                    case 16:
                    case 17:
                        // NE/EN/SW/WS
                        mesh.position.x += .10 * CELL_SIZE
                        mesh.position.z -= -.25 * CELL_SIZE;
                        color = "#aaff00"
                        mesh.rotation.y = -Math.PI/4
                        
                        break;
                    case 5:
                    case 8:
                        // NW/WN/SE/ES
                        color = "#0000ff"
                        mesh.rotation.y = Math.PI/4
                        mesh.position.x += .10 * CELL_SIZE
                        mesh.position.z += -.25 * CELL_SIZE;
                        break;
                    case 15:
                    case 18:
                        mesh.position.x -= .10 * CELL_SIZE
                        mesh.position.z -= -.25 * CELL_SIZE;
                        color = "#00aaff"
                        mesh.rotation.y = Math.PI/4
                        break;
                    case 9:
                        // A puddle :P
                        mesh.scale.x = 2
                        mesh.scale.z = .5
                        color = "#FF0000"
                        break;
                    case 10:
                        // A river mouth ;D
                        mesh.scale.x = 2
                        mesh.scale.z = .5
                        color = "#FF44AA"
                        break;
                    case 11:
                        // A swamp!
                        mesh.scale.x = 2
                        mesh.scale.z = .5
                        color = "#5a6b16"
                        break;                        

                }
                material.color = new THREE.Color(color)
                scene.add(mesh)
                RIVERS.push(mesh)

            }

            // Draw Trees
            var numTrees = parseInt(mapTrees[x][y]);
            if(numTrees > 0) 
            {
                
                var treeHeight = CELL_SIZE * numTrees * .7
    
                colorStr = FOLIAGE_COLORS[numTrees];
                geometry = new THREE.BoxBufferGeometry(CELL_SIZE * .2,treeHeight,CELL_SIZE * .2)
                material = new THREE.MeshPhongMaterial({color: colorStr})
                mesh = new THREE.Mesh(geometry, material)
                mesh.position.x = x * CELL_SIZE
                mesh.position.y = boxHeight + treeHeight * .5
                mesh.position.z = -y * CELL_SIZE

                scene.add(mesh)
                TREES.push(mesh)
            }


            // Draw enemies
            var curEnemy = mapEnemies[x][y];
            if(curEnemy !== null)
            {
                var treeHeight = CELL_SIZE * 15
                geometry = new THREE.BoxBufferGeometry(CELL_SIZE * .2,treeHeight,CELL_SIZE * .2)
                material = new THREE.MeshPhongMaterial({color: "#ff0000"})
                mesh = new THREE.Mesh(geometry, material)
                mesh.position.x = x * CELL_SIZE- CELL_SIZE * .4
                mesh.position.y = boxHeight + treeHeight * .5
                mesh.position.z = -y * CELL_SIZE

                scene.add(mesh)
                ENEMIES.push(mesh)
            }

            // Draw Player Pos

            try
            {
                if(playerPos.x  == x && playerPos.y  == y)
                {
                    var treeHeight = CELL_SIZE * 15
                    geometry = new THREE.BoxBufferGeometry(CELL_SIZE * .2,treeHeight,CELL_SIZE * .2)
                    material = new THREE.MeshPhongMaterial({color: "#00ffff"})
                    mesh = new THREE.Mesh(geometry, material)
                    mesh.position.x = x * CELL_SIZE - CELL_SIZE * .4
                    mesh.position.y = boxHeight + treeHeight * .5
                    mesh.position.z = -y * CELL_SIZE

                    scene.add(mesh)
                    PLAYERS.push(mesh)
                }
            }catch(e)
            {
                //console.error(e);
            }
            
            
        }
    }
}

function LoadMap(data)
{
    mapSize = data["heightMap"].length;
    mapHeights = data["heightMap"];
    mapTrees = data["treeMap"];
    mapRivers = data["riverMap"];
    mapEnemies = data["enemyMap"]
    playerPos = data["playerPosition"]

    // This ensures the map always fills the viewing window
    HEIGHT_SCALAR = CELL_SIZE * .25;

    init()
    ResetView()
}

function CreateKey()
{
    var i = 0;
    colorSize = 100;
    for(color of COLORS)
    {
        push();
        fill(color)
        square(-200, -1100 + i++ * colorSize, colorSize)
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

