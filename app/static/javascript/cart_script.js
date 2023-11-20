document.addEventListener('DOMContentLoaded', function() {
    const decreaseBtns = document.querySelectorAll('.decreaseBtn')
    const increaseBtns = document.querySelectorAll('.increaseBtn')
    const quantityInputs = document.querySelectorAll('.quantityInput')
    const removeBtns = document.querySelectorAll('.removeBtn')
    const orderSubmitBtn = document.getElementById('orderSubmitBtn')

    const saveProdState = (productId, quantity, btnDisabled) => {
        const actionData = {
          quantity: quantity,
          btnDisabled: btnDisabled
        }
        localStorage.setItem(productId, JSON.stringify(actionData))
    }

    const setDataFromLocalStorage = (productId, index) => {
        const storedData = localStorage.getItem(productId)
        if (storedData) {
            const parsedData = JSON.parse(storedData)
            increaseBtns[index].disabled = parsedData.btnDisabled
        }
    }

    const recountMinOrderAmount = () => {
        let totalSum = document.getElementById('total-sum')
        let minSum = totalSum ? parseFloat(totalSum.getAttribute('min-order-amount')) : null
        let errorText = document.getElementById('errorTextFormOrder')
        let orderContainer = document.getElementById('orderContainer')

        if (totalSum && minSum && errorText && orderContainer) {
            if (minSum > parseFloat(totalSum.textContent)) {
                orderContainer.classList.add('hidden')
                errorText.classList.remove('hidden')
            } else if (minSum < parseFloat(totalSum.textContent)) {
                orderContainer.classList.remove('hidden')
                errorText.classList.add('hidden')
            }
        }
    }

    recountMinOrderAmount()

    decreaseBtns.forEach((decreaseBtn, index) => {
        decreaseBtn.addEventListener('click', function() {
            let input = quantityInputs[index]
            const productId = input.getAttribute('product-id')
            let increaseBtn = increaseBtns[index]
            let qtyPrice = document.querySelector(`td[product-id="${productId}"]`)
            let totalSum = document.getElementById('total-sum')

            const form = decreaseBtn.closest('.addToCartForm')
            const formData = new FormData(form)

            let quantity = formData.get('quantity')
            if (quantity > 1) {
                quantity--
                formData.set('quantity', quantity)
                fetch(form.action, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        input.value = quantity
                        increaseBtn.disabled = false
                        saveProdState(productId, quantity, false)
                        qtyPrice.textContent = data.qty_price
                        totalSum.textContent = data.total
                        recountMinOrderAmount()
                    }
                })
                .catch(error => {
                    console.error('Error:', error)
                })
            }
        })
    })

    increaseBtns.forEach((increaseBtn, index) => {
        let input = quantityInputs[index]
        const productId = input.getAttribute('product-id')
        setDataFromLocalStorage(productId, index)
        increaseBtn.addEventListener('click', function() {
            const stock = parseInt(input.getAttribute('max'))

            let qtyPrice = document.querySelector(`td[product-id="${productId}"]`)
            let totalSum = document.getElementById('total-sum')

            let form = increaseBtn.closest('.addToCartForm')
            const formData = new FormData(form)

            let quantity = formData.get('quantity')
            quantity++
            formData.set('quantity', quantity)
            if (quantity === stock) {
                increaseBtn.disabled = true
            }
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    saveProdState(productId, quantity, increaseBtn.disabled)
                    input.value = quantity
                    qtyPrice.textContent = data.qty_price
                    totalSum.textContent = data.total
                    recountMinOrderAmount()
                }
            })
            .catch(error => {
                console.error('Error:', error)
            })
        })
    })

    removeBtns.forEach((removeBtn, index) => {
        let input = quantityInputs[index]
        const productId = input.getAttribute('product-id')
        removeBtn.addEventListener('click', function() {
            localStorage.removeItem(productId)
            let form = removeBtn.parentElement
            if (form) form.submit()
        })
    })

    quantityInputs.forEach((input) => {
        input.addEventListener('input', function() {
            let quantity = parseInt(input.value)
            const stock = parseInt(input.getAttribute('max'))
            const productId = input.getAttribute('product-id')
            let qtyPrice = document.querySelector(`td[product-id="${productId}"]`)
            let totalSum = document.getElementById('total-sum')

            const buttonId = input.getAttribute('button-id')
            let increaseBtn = increaseBtns[parseInt(buttonId)]

            const form = input.closest('.addToCartForm')
            const formData = new FormData(form)

            if (isNaN(quantity) || quantity < 1) {
                quantity = 1
                input.value = quantity
                increaseBtn.disabled = false
                formData.set('quantity', quantity)
            } else if (quantity > stock) {
                quantity = stock
                input.value = quantity
                increaseBtn.disabled = true
                formData.set('quantity', quantity)
            }

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    saveProdState(productId, quantity, increaseBtn.disabled)
                    qtyPrice.textContent = data.qty_price
                    totalSum.textContent = data.total
                    recountMinOrderAmount()
                }
            })
            .catch(error => {
                console.error('Error:', error)
            })
        })
    })

    if (orderSubmitBtn) {
        orderSubmitBtn.addEventListener('click', function(event) {
            event.preventDefault()

            const formOrder = document.getElementById('formOrder')
            let formData = new FormData(formOrder)
            console.log(formOrder)
            console.log(formData)
            fetch(formOrder.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    localStorage.clear()
                }
                window.location = data.redirect
            })
            .catch(error => {
                console.error('Error submitting the form:', error)
            })
        })
    }
})