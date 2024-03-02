const yearDropdown = document.getElementById('year-dropdown');

// Create an option element for "Select Year" as the default option
const defaultOption = document.createElement('option');
defaultOption.value = 'Select Year';
defaultOption.textContent = 'Select Year';
defaultOption.selected = true; 
yearDropdown.appendChild(defaultOption);

// Dynamically generate years for the dropdown
for (let i = 2001; i <= 2050; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    yearDropdown.appendChild(option);
}
