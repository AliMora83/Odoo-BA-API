function checkStudentUser() {
    var userID = localStorage.getItem("StudentId");
    var IsWebLogin = localStorage.getItem('Weblogin');
    if (userID == null) {
        if (IsWebLogin == 'Yes') {
            window.location = "/StudentWeb/Home";
        }
        else {
            window.location = "/AppLogin/Home/StudentLogin";
        }
    }
} 
function checkTeacherUser() {
    var userID = localStorage.getItem("TeacherId");
    if (userID == null) {
        window.location = "/AppLogin/Home/TutorLogin";
    }
}

function TogglePassword(inputId) {
    var inputId = document.getElementById(inputId);
    if (inputId.type === "password") {
        inputId.type = "text";
        $("#eye").attr("class", "input-icon fa fa-eye color-theme");
    } else {
        inputId.type = "password";
        $("#eye").attr("class", "input-icon fa fa-eye-slash color-theme");
    }
}

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
} 

function checkvalues() {
    var isValid = "1"; 
    $("input[required]").each(function () {
        var element = $(this);
        if (element[0].type != "file" && element[0].type != "hidden") {
            if (element.val().trim() === "") {
                isValid = element; 
                return false; 
            }
        }
    });
    if (isValid !== "1") return isValid;

    $("textarea[required]").each(function () {
        var element = $(this);
        if (element.val().trim() === "") {
            isValid = element;
            return false; 
        }
    });
    if (isValid !== "1") return isValid;

    $("select[required]").each(function () {
        var element = $(this);
        if (element.val().trim() === "") {
            isValid = element; 
            return false; 
        }
    });
    return isValid;
}


function setCookie(name, value, expiryDateTime) {
    // Ensure expiryDateTime is a valid Date object
    if (!(expiryDateTime instanceof Date)) {
        console.error("Invalid expiryDateTime. Please provide a valid Date object.");
        return;
    }

    // Convert the date to GMT string
    const expires = "expires=" + expiryDateTime.toUTCString();

    // Set the cookie
    document.cookie = `${name}=${value}; ${expires}; path=/;`;
}

function getCookie(name) {
    const cookieString = document.cookie; // Get all cookies as a single string
    const cookies = cookieString.split("; "); // Split into individual cookies

    // Find the cookie with the matching name
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const [cookieName, cookieValue] = cookie.split("="); // Split name and value
        if (cookieName === name) {
            return decodeURIComponent(cookieValue); // Return the decoded value
        }
    }

    return null; // Return null if the cookie isn't found
}

function formatTimeSpanWithAmPm(timeSpan) {
    // Split the TimeSpan (e.g., "15:30:00") into hours, minutes, seconds
    const [hours, minutes] = timeSpan.split(':').map(Number);

    // Determine AM or PM
    const period = hours >= 12 ? "PM" : "AM";

    // Convert to 12-hour format
    const hour12 = hours % 12 || 12; // 12-hour format (0 becomes 12)

    // Format as "hh:mm AM/PM"
    return `${hour12}:${minutes.toString().padStart(2, '0')} ${period}`;
}

// Example usage
const timeSpan = "15:30:00"; // Example TimeSpan string
const formattedTime = formatTimeSpanWithAmPm(timeSpan);

function validatePasswords() {
    const password = document.getElementById('Password').value;
    const confirmPassword = document.getElementById('ConfirmPassword').value;
    const messageElement = document.getElementById('message');
    messageElement.textContent = '';
    if (!password || !confirmPassword) {
        messageElement.textContent = 'Both password fields must be filled out.';
        messageElement.className = 'color-red';
        return;
    }
    if (password === confirmPassword) {
        messageElement.textContent = 'Passwords match!';
        messageElement.className = 'color-green';
    } else {
        messageElement.textContent = 'Passwords do not match.';
        messageElement.className = 'color-red';
        document.getElementById('ConfirmPassword').value = "";
    }
}

function changetype(dateinput) {
    dateinput.type = "date";
}

function convertUTCToLocal(date,time, localTimeZone) {   

    var dateTime = `${date}T${time}Z`;
    var datetimeUTC = new Date(dateTime);

    const utcDate = new Date(datetimeUTC);
    const localDate = new Date(
        utcDate.toLocaleString("en-US", { timeZone: localTimeZone })
    );
    return localDate;
}


function populateFilters() {
    $.ajax({
        url: '/api/CustomerApi/GetSearchFilters',
        method: 'GET', 
        dataType: 'json',
        success: function (response) {
            if (response) {
                // Populate CountryID select
                let countrySelect = $('#CountryID');
                countrySelect.empty(); // Clear existing options
                countrySelect.append('<option value="">Select Country</option>'); // Default option
                $.each(response.CountryID, function (index, country) {
                    countrySelect.append(`<option value="${country.Id}">${country.CountryName}</option>`);
                });

                // Set selected value for CountryID from localStorage
                let storedCountryID = localStorage.getItem('CountryID');
                if (storedCountryID) {
                    countrySelect.val(storedCountryID);
                }
                
                // Populate RatingID select
                let ratingSelect = $('#RatingID');
                ratingSelect.empty(); // Clear existing options
                ratingSelect.append('<option value="">Select Rating</option>'); // Default option
                $.each(response.RatingID, function (index, rating) {
                    ratingSelect.append(`<option value="${rating.Rating}">${rating.RatingText}</option>`);
                });

                // Set selected value for RatingID from localStorage
                let storedRatingID = localStorage.getItem('RatingID');
                if (storedRatingID) {
                    ratingSelect.val(storedRatingID);
                }
            }
        },
        error: function (xhr, status, error) {
            console.error('Failed to fetch filters:', error);
        }
    });
}

function searchCourses() {
    // Get filter values    
    let keyword = $('#mysearch').val();
    let countryID = $('#CountryID').val();
    let ratingID = $('#RatingID').val();

    // Build the query parameters
    let queryParams = {
        keyword: keyword || '', // Default to empty string if not provided
        CountryID: countryID || null, // Default to null if not selected
        RatingID: ratingID || null // Default to null if not selected
    };

    // Make an AJAX request to the API
    $.ajax({
        url: '/api/CustomerApi/SearchCourse', // Replace with the correct API URL
        method: 'GET',
        data: queryParams,
        dataType: 'json',
        success: function (response) {
            if (response) {
                let resultContainer = $('#divproducts'); // Assuming there's a div with this ID for results
                resultContainer.empty(); // Clear previous results

                if (response.length > 0) {
                    // Loop through the response and append each course
                    $.each(response, function (index, course) {
                        resultContainer.append(`<a href="/StudentApp/Home/SearchCourseDetails?cid=${course.Id}" class="search-result-list"><img class="shadow-l preload-img" src="${course.ProfilePicture}" alt="Photo"><img class="search-flag shadow-l preload-img" src="${course.FlagImage}" alt="Flag"><p class="mb-0">By: ${course.TutorName}</p><h1>${course.CourseName}</h1><h4 style="line-height: 18px;"><span class="product-reviews-summary"><span class="rating-summary"><span class="rating-result"> <span style="width:${course.AverageRating}%"><span>${course.AverageRating}</span>% of <span>100</span></span></span></span></span></h4><h4 class="font-500 font-14 mb-1">Course Fee: $${course.Fee}</h4></a>`);
                    });
                    $('#pCount').html(response.length + ' Course(s) found');
                } else {
                    $('#pCount').html('');
                    resultContainer.append('<div><h5 style="text-align:center">No Course found...</h5></div>');
                }
            }
        },
        error: function (xhr, status, error) {
            console.error('Failed to fetch courses:', error);
        }
    });
}

function clearFilters() {
    localStorage.removeItem("RatingID");
    $('#RatingID').val('');
    searchCourses();
}