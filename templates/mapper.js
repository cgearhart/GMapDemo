(function(ns, $, google) {

    var

    target_id,


    map = {

        drawMap: function () {

            var options = {
                center: this.center,
                zoom: this.zoom,
                maxZoom: 5,
                minZoom: 5,
                disableDefaultUI: true,
                scrollwheel: false,
                keyboardShortcuts: false,
                draggable: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            if ( !this.handle ) {
                this.handle = new google.maps.Map(window.document.getElementById(this.target_id), options);
            } else {
                this.handle.panTo(this.center);  // Always try returning to center - does nothing if already centered
                if ( this.zoom != this.handle.getZoom() ) {  // Redraws whole map - only try if zoom has changed
                    this.handle.setZoom(this.zoom);
                }
            }
        },

        drawMarkers: function () {
            // get markers from database
            $.get("http://teslascdemo.herokuapp.com/stations/",
                function( data ) {
                    // add each marker to the map
                    alert(data);
                    for (var station in data) {
                        var location = new google.maps.LatLng(station.lat, station.lng);
                        var icon = null;
                        switch (station.status) {
                            case "Operational":
                                icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png";
                                break;
                            case "Scheduled Maintenance":
                                icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png";
                                break;
                            case "Unscheduled Maintenance":
                                icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/yellow-dot.png";
                                break;
                            case "Out of Service":
                                icon = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";
                                break;
                        }
                        marker.draw(location, icon);
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


    marker = {
        draw: function (location, icon) {
            if (this.handle) this.handle.setMap(null);  // clear the marker from the map if already defined

            var options = {
                draggable: false,
                visible: true,
                position: location,
                map: map.handle,
                icon: icon
            };

            this.handle = new google.maps.Marker(options);
        }
    };


    // Initialize the app

    // Need public method to initialize the app using "body onload"; otherwise id=map_canvas doesn't exist & causes error
    ns.mapper = {
        
        initialize: function (target_id) {
            map.initialize(target_id);
        }
    };

})(this, jQuery, google);
