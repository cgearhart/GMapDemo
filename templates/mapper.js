(function(ns, $, google) {

    var

    // div name from the DOM to insert the map object
    target_id,

    // google map object
    map = {

        drawMap: function () {

            // draw a map approximately centered on the united states and 
            // override default map options to disable user interaction
            var options = {
                center: new google.maps.LatLng(38, -98),
                zoom: 5,
                disableDefaultUI: true,
                scrollwheel: false,
                keyboardShortcuts: false,
                draggable: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var div_handle = window.document.getElementById(this.target_id);
            this.handle = new google.maps.Map(div_handle, options);

            // make sure the map shows all of the supercharger stations
            var sw = new google.maps.LatLng(24.20689,-126.927795);
            var ne = new google.maps.LatLng(49.667628,-66.459045);
            var bounds = new google.maps.LatLngBounds(sw, ne);
            this.handle.fitBounds(bounds);

        },

        drawMarkers: function () {
            // GET request for station marker locations from the REST API
            var url = "http://teslascdemo.herokuapp.com/stations/";
            $.get(url, function( data ) {
                    
                // add each marker to the map
                for (var idx = 0; idx < data.length; idx++) {
                    var station = data[idx];
                    var location = new google.maps.LatLng(station.lat,
                                                          station.lon);
                    
                    // chanage the color of the marker icon based on the
                    // station health record
                    var icon = null;
                    switch (station.stat.toLowerCase()) {
                        case "op":
                            icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png";
                            break;
                        case "sm":
                            icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png";
                            break;
                        case "um":
                            icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/yellow-dot.png";
                            break;
                        case "os":
                            icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";
                            break;
                        default:
                            icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png";
                            break;
                    }

                    var options = {
                        draggable: false,
                        visible: true,
                        position: location,
                        map: map.handle,
                        icon: icon
                    };
                    markers.push(new google.maps.Marker(options));
                }
            });
        },

        initialize: function (target_id) {

            this.target_id = this.target_id || target_id;
            this.drawMap();
            this.drawMarkers();
        }
    },

    // must keep marker handles in an array in order for the objects to persist
    // and be displayed on the map
    markers = [];

    // Initialize the app
    // Need public method to initialize the app using "body onload"; 
    // otherwise id=map_canvas doesn't exist & causes error
    ns.mapper = {
        
        initialize: function (target_id) {
            map.initialize(target_id);
        }
    };

})(this, jQuery, google);
