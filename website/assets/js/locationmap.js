let map, marker;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 5,
    });
}
function showCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                // Only set display once
                document.getElementById("pRadius").innerText = "This area covers approximately 0 to 10 KM radius.";
                if (document.getElementById("map").style.display !== "block") {
                    document.getElementById("map").style.display = "block";
                }

                // Force map to recalc size to avoid fullscreen issue
                google.maps.event.trigger(map, "resize");

                let currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                map.setCenter(currentLocation);
                map.setZoom(15);

                if (marker) marker.setMap(null);

                marker = new google.maps.Marker({
                    position: currentLocation,
                    map: map,
                    title: "You are here!"
                });
            },
            function () {
                alert("Geolocation failed!");
            }
        );
    } else {
        alert("Your browser doesn't support geolocation.");
    }
}

var circle;
function setareaID(areaid, areaname) {
    console.log(areaname);
    var settings = {
        "url": "/api/HomeApi/GetAreasDetails?areaid=" + areaid,
        "method": "GET",
        "timeout": 0,
    };
    $.ajax(settings).done(function (response) {
        if (response != null) {
            if (document.getElementById("map").style.display !== "block") {
                document.getElementById("map").style.display = "block";
            }
            document.getElementById("pRadius").innerText = "This area covers approximately " + response.AreaRadius + " KM radius.";
            let Latitude = parseFloat(response.Latitude);
            let Longitude = parseFloat(response.Longitude);
            let position = { lat: Latitude, lng: Longitude };

            var zoomvar = response.AreaRadius+1;
            // Move map to new location
            map.setCenter(position);
            map.setZoom(zoomvar);

            // Remove old marker if exists
            if (marker) {
                marker.setMap(null);
            }

            // Remove old circle if exists
            if (circle) {
                circle.setMap(null);
            }

            // Add new marker
            marker = new google.maps.Marker({
                position: position,
                map: map,
                title: areaname
            });

            // Draw blue circle
            circle = new google.maps.Circle({
                strokeColor: '#0000FF',      // border color
                strokeOpacity: 0.8,          // border opacity
                strokeWeight: 2,             // border width
                fillColor: '#0000FF',        // fill color
                fillOpacity: 0.15,           // fill opacity (transparent)
                map: map,
                center: position,
                radius: response.AreaRadius * 1000 // convert KM to meters
            });
        }
    });
}
 
function getCitiesbyProvince(provinceId) {
    $('#hdAreaID').val('');
    $('#txtAddress').val('');
    $('#divarearesult').html('');
    $('#CityID').empty().append('<option value="">Select Your City/Town</option>');
    if (provinceId) {
        $.ajax({
            url: '/api/HomeApi/GetCitiesByProvince',
            type: 'GET',
            data: { pid: provinceId },
            success: function (data) {
                if (data.length > 0) {
                    $.each(data, function (i, item) {
                        $('#CityID').append($('<option>', {
                            value: item.Id,
                            text: item.CityName
                        }));
                    });
                }
                else {
                    $('#CityID').empty().append('<option value="">No Cities/Town found</option>');
                }
            }
        });
    }
} 

function getCities() {
    $('#hdAreaID').val('');
    $('#txtAddress').val('');
    $('#divarearesult').html('');   
    $('#CityID').empty().append('<option value="">Select Your City/Town</option>');
    $.ajax({
        url: '/api/HomeApi/GetAllCities',
        type: 'GET',
        success: function (data) {
            if (data.length > 0) {
                $.each(data, function (i, item) {
                    $('#CityID').append($('<option>', {
                        value: item.Id,
                        text: item.CityName
                    }));
                });
            }
            else {
                $('#CityID').empty().append('<option value="">No Cities/Town found</option>');
            }
        }
    });
}

function getAreaSuburb(cityId) {   
    $('#hdAreaID').val('');
    $('#txtAddress').val('');
    $('#divarearesult').html('');
    $('#PostalCodeID').empty().append('<option value="">Select Your Area/Suburb</option>');
    if (cityId) {
        $.ajax({
            url: '/api/HomeApi/GetAreasByCity',
            type: 'GET',
            data: { cityId: cityId },
            success: function (data) {
                if (data.length > 0) {
                    $.each(data, function (i, item) {
                        $('#PostalCodeID').append($('<option>', {
                            value: item.Id,
                            text: item.AreaName
                        }));
                    });
                }
                else {
                    $('#PostalCodeID').empty().append('<option value="">No Area/Suburb found</option>');
                }
            }
        });
    }
}