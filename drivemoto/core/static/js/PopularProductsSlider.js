document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".products__tab");
    const productSliderContainer = document.querySelector(".product__slider");

    tabs.forEach(tab => {
        tab.addEventListener("click", function(event) {
            event.preventDefault();

            const categoryId = this.getAttribute("data-category-id"); // Получаем ID категории

            // Удаляем активный класс с других табов
            tabs.forEach(t => t.classList.remove("tab--active"));
            // Добавляем активный класс на выбранный таб
            this.classList.add("tab--active");

            // Отправляем AJAX запрос
            fetch(`/get_products_by_category/${categoryId}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Ошибка загрузки товаров");
                }
                return response.text(); // Возвращаем HTML как текст
            })
            .then(html => {
                // Заменяем содержимое слайдера товара на новый HTML
                productSliderContainer.innerHTML = html;
            })
            .catch(error => {
                console.error("Ошибка:", error);
                alert("Ошибка загрузки товаров");
            });
        });
    });
});