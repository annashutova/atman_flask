document.addEventListener('DOMContentLoaded', function() {
    const decreaseBtns = document.querySelectorAll('.decreaseBtn')
    const increaseBtns = document.querySelectorAll('.increaseBtn')
    const quantityInputs = document.querySelectorAll('.quantityInput')

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

    const saveQuantity = (productId, quantity) => {
        const actionData = {
          quantity: quantity,
        }
        localStorage.setItem(productId, JSON.stringify(actionData))
    }

    const setQuantityFromLocalStorage = (productId, index) => {
        const storedData = localStorage.getItem(productId)
        if (storedData) {
            const parsedData = JSON.parse(storedData)
            quantityInputs[index].value = parsedData.quantity

            const buyButton = document.querySelector(`button[button-id="${index}"]`)
            changeButtonState(buyButton, true)
        }
    }

    quantityInputs.forEach((input, index) => {
        const productId = input.getAttribute('product-id')
        setQuantityFromLocalStorage(productId, index)
    })

    document.addEventListener('click', function (event) {
        if (event.target && event.target.matches('.btn.btn-danger')) {
            let buyButton = event.target
            const form = buyButton.closest('.addToCartForm')

            const formData = new FormData(form)
            const productId = buyButton.getAttribute('product-id')

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    let quantity = formData.get('quantity')
                    saveQuantity(productId, quantity)
                    changeButtonState(buyButton, true)
                }
            })
            .catch(error => {
                console.error('Error:', error)
            })
        }
    })

    decreaseBtns.forEach((decreaseBtn, index) => {
        decreaseBtn.addEventListener('click', function() {
            let quantity = parseInt(quantityInputs[index].value)
            let buyButton = document.querySelector(`button[button-id="${index}"]`)
            changeButtonState(buyButton, false)
            if (quantity > 1) {
                quantity--
                quantityInputs[index].value = quantity
            }
        })
    })

    increaseBtns.forEach((increaseBtn, index) => {
        increaseBtn.addEventListener('click', function() {
            let quantity = parseInt(quantityInputs[index].value)
            let buyButton = document.querySelector(`button[button-id="${index}"]`)
            changeButtonState(buyButton, false)
            quantity++
            quantityInputs[index].value = quantity
        })
    })

    quantityInputs.forEach((input) => {
        input.addEventListener('input', function() {
            let quantity = parseInt(input.value)
            const buttonId = input.getAttribute('button-id')
            let buyButton = document.querySelector(`button[button-id="${buttonId}"]`)
            changeButtonState(buyButton, false)
            if (isNaN(quantity) || quantity < 1) {
                input.value = 1
            }
        })
    })
})