document.addEventListener('DOMContentLoaded', function() {
    let increaseBtn = document.getElementById('increaseBtn')
    let decreaseBtn = document.getElementById('decreaseBtn')
    let quantityInput = document.getElementById('quantityInput')
    let buyButton = document.getElementById('buyBtn')

    const productId = buyButton.getAttribute('product-id')

    const changeButtonState = (button, buttonClicked) => {
        if (buttonClicked) {
            button.textContent = 'В корзину'
            button.onclick = function() {
                window.location = button.getAttribute('redirect-url')
            }
        } else {
            button.onclick = null
            button.textContent = 'Купить'
        }
    }

    const saveProdState = (productId, quantity, btnDisabled) => {
        const actionData = {
          quantity: quantity,
          btnDisabled: btnDisabled
        }
        localStorage.setItem(productId, JSON.stringify(actionData))
    }

    const setDataFromLocalStorage = (productId) => {
        const storedData = localStorage.getItem(productId)
        if (storedData) {
            const parsedData = JSON.parse(storedData)
            quantityInput.value = parsedData.quantity
            increaseBtn.disabled = parsedData.btnDisabled
            changeButtonState(buyButton, true)
        }
    }

    const checkQuantity = () => {
        let quantity = parseInt(quantityInput.value)
        const stock = parseInt(quantityInput.getAttribute('max'))
        if (quantity === stock) {
            increaseBtn.disabled = true
        }
    }

    checkQuantity()
    setDataFromLocalStorage(productId)

    buyButton.addEventListener('click', function () {
        const form = buyButton.closest('.addToCartForm')
        const formData = new FormData(form)

        let btnDisabled = increaseBtn.disabled

        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                let quantity = formData.get('quantity')
                saveProdState(productId, quantity, btnDisabled)
                changeButtonState(buyButton, true)
            }
        })
        .catch(error => {
            console.error('Error:', error)
        })
    })

    decreaseBtn.addEventListener('click', function() {
        let quantity = parseInt(quantityInput.value)
        changeButtonState(buyButton, false)
        if (quantity > 1) {
            quantity--
            quantityInput.value = quantity
            increaseBtn.disabled = false
        }
    })

    increaseBtn.addEventListener('click', function() {
        const stock = parseInt(quantityInput.getAttribute('max'))
        let quantity = parseInt(quantityInput.value)
        changeButtonState(buyButton, false)
        quantity++
        quantityInput.value = quantity
        if (quantity === stock) {
            increaseBtn.disabled = true
        }
    })

    quantityInput.addEventListener('input', function() {
        let quantity = parseInt(quantityInput.value)
        const stock = parseInt(quantityInput.getAttribute('max'))
        changeButtonState(buyButton, false)
        if (isNaN(quantity) || quantity < 1) {
            quantityInput.value = 1
            increaseBtn.disabled = false
        } else if (quantity >= stock) {
            quantityInput.value = stock
            increaseBtn.disabled = true
        }
    })
})