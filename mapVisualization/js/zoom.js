function zoom(event) {
    // zoom according to direction of mouseWheelDeltaY rather than value
    let sensitivityZoom = 0.05;
    let scaleFactor = c.height;
    if (event.deltaY > 0) {
    c._curCamera._orbit(0, 0, sensitivityZoom * scaleFactor);
    } else {
    c._curCamera._orbit(0, 0, -sensitivityZoom * scaleFactor);
    }
    }

document.onkeypress =(e) =>
{
    switch(e.key)
    {
        case "v":
        case "V":
            TogglePlayers()
            break;
        case "t":
        case "T":
            ToggleTrees()
            break;
        case "r":
        case "R":
            ToggleRivers()
            break;
        case "e":
        case "E":
            ToggleEnemies()
            break;   
        case "f":         
        case "F":         
            ToggleWaterFeatures()
            break;
        // space
        case " ":
            ResetView();
            break;



    }
}

window.addEventListener( 'resize', onWindowResize, false );

function onWindowResize(){

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

}

document.getElementById("save").onclick = () =>
{
    REQUEST_SAVE = true
}