document.addEventListener('DOMContentLoaded', function () {
    let searchInput = document.getElementById('search-input')
    let searchResults = document.getElementById('search-results')
    let cardDropdown = document.getElementById('card-dropdown')

    function updateResults(results) {
        searchResults.innerHTML = ''

        results.forEach(function (result) {
            if (result.type === 'header') {
                let item = document.createElement('div')
                item.classList.add('result-header')

                let header = document.createElement('h5')
                header.textContent = result.title
                header.classList.add('mt-3')
                let divider = document.createElement('div')
                divider.classList.add('red-divider')

                item.appendChild(header)
                item.appendChild(divider)
                searchResults.appendChild(item)
            } else {
                let item = document.createElement('div')
                item.classList.add('result-item')

                let link = document.createElement('a')
                link.setAttribute('href', result.url)
                link.classList.add('nav-link', 'px-3', 'link-dark')
                link.textContent = result.title

                item.appendChild(link)
                searchResults.appendChild(item)
            }
        })

        cardDropdown.style.display = 'block'
        searchResults.style.display = 'block'
    }

    searchInput.addEventListener('input', function () {
        let query = this.value

        fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => updateResults(data))
        .catch(error => console.log('Error while fetching search results:', error))
    })

    document.addEventListener('click', function (event) {
        if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
            cardDropdown.style.display = 'none'
            searchResults.style.display = 'none'
        }
    })
})