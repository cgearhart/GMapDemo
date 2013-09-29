(function(ns, $, google) {

    var

    target_id,


    map = {

        drawMap: function () {

            var options = {
                center: this.center,
                // zoom: this.zoom,
                // maxZoom: 5,
                // minZoom: 5,
                disableDefaultUI: true,
                scrollwheel: false,
                keyboardShortcuts: false,
                draggable: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            this.handle = new google.maps.Map(window.document.getElementById(this.target_id), options);

            var sw = new google.maps.LatLng(24.20689,-126.927795);
            var ne = new google.maps.LatLng(49.667628,-66.459045);
            var bounds = new google.maps.LatLngBounds(sw, ne);
            this.handle.fitBounds(bounds);

        },

        drawMarkers: function () {
            // get markers from database
            // add info window: http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example
            $.get("http://teslascdemo.herokuapp.com/stations/",
                function( data ) {
                    // add each marker to the map
                    for (var idx = 0; idx < data.length; idx++) {
                        var station = data[idx];
                        var location = new google.maps.LatLng(station.lat,
                                                              station.lon);
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

            // set default values if undefined or wrong type
            if ( typeof this.center !== typeof new google.maps.LatLng() ) {
                // default to approximately the center of the USA
                this.center =  new google.maps.LatLng(38, -98);
            }

            this.zoom = this.zoom || 5;  // set default zoom level
            this.drawMap();
            this.drawMarkers();
        }
    },

    markers = new Array();

    // Initialize the app
    // Need public method to initialize the app using "body onload"; otherwise id=map_canvas doesn't exist & causes error
    ns.mapper = {
        
        initialize: function (target_id) {
            map.initialize(target_id);
        }
    };

})(this, jQuery, google);
