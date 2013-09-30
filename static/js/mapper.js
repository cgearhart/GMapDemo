(function(ns, $, google) {

    // must keep handles in scope for the objects to persist and be displayed
    var map_handle, infowindow,
    marker_handles = [];

    // Initialize the app; Need public method to initialize the app using 
    // "body onload", otherwise id=map_canvas doesn't exist & causes error
    ns.mapper = {

        drawMap: function (target_div_id) {
            // Use the Google Maps API to draw a map in the target div id of
            // the DOM, and fit the view to the bounds of the continental 
            // United States, returning the handle of the created object.

            var sw, ne, bounds;
            var div_handle, handle;

            // draw a map approximately centered on the united states and 
            // override default map options to disable user interaction
            var options = {
                center: new google.maps.LatLng(49, -158.25),
                scrollwheel: false,
                keyboardShortcuts: false,
                draggable: false,
                disableDoubleClickZoom: true,
                disableDefaultUI: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            div_handle = window.document.getElementById(target_div_id);
            handle = new google.maps.Map(div_handle, options);

            // make sure the map shows all of the supercharger stations
            sw = new google.maps.LatLng(24,-125);
            ne = new google.maps.LatLng(50,-66.5);
            bounds = new google.maps.LatLngBounds(sw, ne);
            handle.fitBounds(bounds);
            return handle;

        },

        drawMarkers: function (map_handle) {
            // Use the Google Maps API and teslascdemo API to add markers
            // representing each station in the teslascdemo database to the
            // map controlled by map_handle

            // GET request for station marker locations from the REST API
            var url = "http://teslascdemo.herokuapp.com/stations/";
            $.get(url, function( data ) {
                    
                // add each marker to the map
                for (var idx = 0; idx < data.length; idx++) {
                    var location, icon, options, marker;

                    location = new google.maps.LatLng(data[idx].lat,
                                                          data[idx].lon);
                    
                    // set the marker icon color according to station health
                    switch (data[idx].stat.toLowerCase()) {
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

                    options = {
                        visible: true,
                        clickable: true,
                        position: location,
                        map: map_handle,
                        icon: icon
                    };
                    marker = new google.maps.Marker(options);
                    marker_handles.push(marker);

                    google.maps.event.addListener(marker, 'click', (function(marker, d) {
                        return function() {
                            var coords = [d.lat, d.lon];
                            if (typeof infowindow != "undefined") {
                                infowindow.close();
                            }
                            infowindow = new google.maps.InfoWindow();
                            infowindow.setContent(coords.join(", "));
                            infowindow.open(map_handle, marker);
                        };
                    })(marker, data[idx]));
                }

            });
        },

        initialize: function (target_id) {

            this.map_handle = this.drawMap(target_id);
            this.drawMarkers(this.map_handle);
        }
    };

})(this, jQuery, google);
