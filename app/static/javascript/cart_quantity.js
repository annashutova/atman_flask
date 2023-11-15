document.addEventListener('DOMContentLoaded', function() {
    const decreaseBtns = document.querySelectorAll('.decreaseBtn')
    const increaseBtns = document.querySelectorAll('.increaseBtn')
    const quantityInputs = document.querySelectorAll('.quantityInput')

    const saveQuantity = (productId, quantity) => {
        const actionData = {
          quantity: quantity,
        }
        localStorage.setItem(productId, JSON.stringify(actionData))
    }

    decreaseBtns.forEach((decreaseBtn, index) => {
        decreaseBtn.addEventListener('click', function() {
            let input = quantityInputs[index]
            let quantity = parseInt(input.value)
            const productId = input.getAttribute('product-id')
            if (quantity > 1) {
                quantity--
                saveQuantity(productId, quantity)
                let form = decreaseBtn.parentElement
                if (form) form.submit()
            }
        })
    })

    increaseBtns.forEach((increaseBtn, index) => {
        increaseBtn.addEventListener('click', function() {
            let input = quantityInputs[index]
            let quantity = parseInt(input.value)
            const productId = input.getAttribute('product-id')
            quantity++
            saveQuantity(productId, quantity)
            let form = increaseBtn.parentElement
            if (form) form.submit()
        })
    })

    quantityInputs.forEach((input) => {
        input.addEventListener('input', function() {
            let quantity = parseInt(input.value)
            const productId = input.getAttribute('product-id')
            if (isNaN(quantity) || quantity < 1) {
                quantity = 1
            }
            saveQuantity(productId, quantity)
            let form = input.parentElement
            if (form) form.submit()
        })
    })
})