// ...existing code...

let favorites = [];

async function loadFavorites() {
    try {
        const response = await fetch('favorites.json');
        const data = await response.json();
        favorites = data.favorites;
        updateFavoritesDropdown();
    } catch (error) {
        console.error('Error loading favorites:', error);
    }
}

function updateFavoritesDropdown() {
    const dropdown = document.getElementById('favoritesDropdown');
    dropdown.innerHTML = '<option value="">Select a favorite city</option>';
    favorites.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        dropdown.appendChild(option);
    });
}

async function saveFavorites() {
    try {
        const response = await fetch('favorites.json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ favorites })
        });
    } catch (error) {
        console.error('Error saving favorites:', error);
    }
}

function toggleFavorite() {
    const city = document.querySelector('.city').textContent;
    const starBtn = document.getElementById('favoriteBtn');
    
    if (favorites.includes(city)) {
        favorites = favorites.filter(f => f !== city);
        starBtn.classList.remove('active');
    } else {
        favorites.push(city);
        starBtn.classList.add('active');
    }
    
    saveFavorites();
    updateFavoritesDropdown();
}

// Add event listeners
document.addEventListener('DOMContentLoaded', loadFavorites);
document.getElementById('favoriteBtn').addEventListener('click', toggleFavorite);
document.getElementById('favoritesDropdown').addEventListener('change', (e) => {
    if (e.target.value) {
        document.querySelector('.search-box input').value = e.target.value;
        checkWeather(e.target.value);
    }
});

// Update existing checkWeather function to update star button
const checkWeather = async (city) => {
    // ...existing code...
    document.getElementById('favoriteBtn').classList.toggle('active', favorites.includes(city));
    // ...existing code...
}
