// Create a WorldWindow for the canvas.
var wwd = new WorldWind.WorldWindow("canvasOne");
var goToAnimator = new WorldWind.GoToAnimator(wwd);


wwd.addLayer(new WorldWind.BMNGLayer());
wwd.addLayer(new WorldWind.BMNGLandsatLayer());
wwd.addLayer(new WorldWind.BingAerialLayer());
wwd.addLayer(new WorldWind.BingAerialWithLabelsLayer());
wwd.addLayer(new WorldWind.AtmosphereLayer());

wwd.addLayer(new WorldWind.CoordinatesDisplayLayer(wwd));
// wwd.addLayer(new WorldWind.ViewControlsLayer(wwd));

// Add a 
document.getElementById('searchButton').addEventListener('click', function() {
    const searchText = document.getElementById('searchText').value;
    console.log('Search:', searchText);

    const coords = searchText.split(',').map(coord => parseFloat(coord.trim()));
    
    if (coords.length === 2 && !isNaN(coords[0]) && !isNaN(coords[1])) {
            markPlace(coords[0], coords[1]);
            addPolygonAtLocation(coords[0], coords[1])
    } else {
            console.error('Invalid coordinates:', searchText);
    }
});


function markPlace(latitude, longitude) {
    var placemarkLayer = new WorldWind.RenderableLayer();
    wwd.addLayer(placemarkLayer);

    var placemarkAttributes = new WorldWind.PlacemarkAttributes(null);
    placemarkAttributes.imageOffset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.3,
        WorldWind.OFFSET_FRACTION, 0.0
    );

    placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.5,
        WorldWind.OFFSET_FRACTION, 1.0
    );

    placemarkAttributes.imageSource = WorldWind.configuration.baseUrl + "images/pushpins/plain-red.png";

    var position = new WorldWind.Position(latitude, longitude, 800000.0);

    var placemark = new WorldWind.Placemark(position, false, placemarkAttributes);

    placemark.label = "Placemark\n" +
        "Lat " + placemark.position.latitude.toPrecision(4).toString() + "\n" +
        "Lon " + placemark.position.longitude.toPrecision(5).toString();
    placemark.alwaysOnTop = true;

    placemarkLayer.addRenderable(placemark);

    goToAnimator.goTo(position);
}

// Example usage

function addPolygonAtLocation(latitude, longitude) {
    // Create a new layer for the polygon
    var polygonLayer = new WorldWind.RenderableLayer();
    wwd.addLayer(polygonLayer);

    // Set the polygon attributes
    var polygonAttributes = new WorldWind.ShapeAttributes(null);
    polygonAttributes.interiorColor = new WorldWind.Color(0, 1, 1, 0.75); // Cyan fill
    polygonAttributes.outlineColor = WorldWind.Color.BLUE; // Blue outline
    polygonAttributes.drawOutline = true;
    polygonAttributes.applyLighting = true;

    // Create boundaries for the polygon to approximate a circle
    var boundaries = [];
    var numberOfPoints = 12; // Number of points to approximate the circle
    var radius = 2.0; // Radius for the circle

    for (var i = 0; i < numberOfPoints; i++) {
        var angle = (i / numberOfPoints) * 2 * Math.PI; // Calculate the angle in radians
        var offsetLat = radius * Math.sin(angle); // Latitude offset
        var offsetLon = radius * Math.cos(angle); // Longitude offset

        boundaries.push(new WorldWind.Position(latitude + offsetLat, longitude + offsetLon, 700000.0));
    }

    // Close the polygon by adding the first point at the end
    boundaries.push(boundaries[0]);

    // Create the polygon with the specified boundaries and attributes
    var polygon = new WorldWind.Polygon(boundaries, polygonAttributes);
    polygon.extrude = true; // This will make the polygon extrude upwards
    polygonLayer.addRenderable(polygon);

    // Redraw the WorldWindow to show the new polygon
    wwd.redraw();
}







// Add WMS imagery
var serviceAddress = "https://neo.sci.gsfc.nasa.gov/wms/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0";
var layerName = "MOD_LSTD_CLIM_M";

var createLayer = function (xmlDom) {
    var wms = new WorldWind.WmsCapabilities(xmlDom);
    var wmsLayerCapabilities = wms.getNamedLayer(layerName);
    var wmsConfig = WorldWind.WmsLayer.formLayerConfiguration(wmsLayerCapabilities);
    var wmsLayer = new WorldWind.WmsLayer(wmsConfig);
    wwd.addLayer(wmsLayer);
};

var logError = function (jqXhr, text, exception) {
    console.log("There was a failure retrieving the capabilities document: " +
        text +
    " exception: " + exception);
};

$.get(serviceAddress).done(createLayer).fail(logError);