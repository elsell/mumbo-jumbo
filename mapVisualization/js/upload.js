window.onload = function() {
    var fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', function(e) {
        var file = fileInput.files[0];
        var textType; // This can be regex to filter file types
        if (file.type.match(textType)) {
            var reader = new FileReader();

            reader.onload = function(e) {
                try{
                    data = JSON.parse(reader.result);    
                    LoadMap(data);
                }catch(e)
                {
                    console.error(e);
                    alert("Cannot load this file. Please try a different file.");
                }
            }

            reader.readAsText(file);	
        } else {
            alert("File not supported!");
        }
    });
}

