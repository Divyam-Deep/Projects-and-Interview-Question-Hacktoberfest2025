// ==============================
// DIGITAL CLOCK (Console Version)
// ==============================

// Function to display current time
function showTime() {
    // Create a new Date object to get the current time
    let currentTime = new Date();

    // Extract hours, minutes, and seconds
    let hours = currentTime.getHours();
    let minutes = currentTime.getMinutes();
    let seconds = currentTime.getSeconds();

    // Format time to show 2 digits (e.g., 07 instead of 7)
    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    // Create a time string in HH:MM:SS format
    let timeString = `${hours}:${minutes}:${seconds}`;

    // Clear the console to display only the updated time each second
    console.clear();

    // Display the current time on the console
    console.log("Current Time: " + timeString);
}

// Call showTime() every 1000 milliseconds (1 second)
setInterval(showTime, 1000);

// Initial call so it shows time instantly without waiting for 1 second
showTime();