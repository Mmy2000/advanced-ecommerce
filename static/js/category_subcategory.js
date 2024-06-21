document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');
    subcategorySelect.classList.add('d-none')

    categorySelect.addEventListener('change', function () {
        const categoryId = this.value;
        console.log(`Fetching subcategories for category ID: ${categoryId}`);

        fetch(`/products/load-subcategories/?category_id=${categoryId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                subcategorySelect.classList.replace('d-none' , 'd-block')
                return response.json();
            })
            .then(data => {
                subcategorySelect.innerHTML = '<option value="">---------</option>';
                data.forEach(subcategory => {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subcategorySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});
