document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!categorySelect || !subcategorySelect) {
        console.error('Category or Subcategory select element not found');
        return;
    }

    categorySelect.addEventListener('change', function () {
        const categoryId = this.value;
        console.log(`Fetching subcategories for category ID: ${categoryId}`);

        // Disable the subcategory select element
        subcategorySelect.disabled = true;
        console.log('Subcategory select element disabled');

        fetch(`/products/load-subcategories/?category_id=${categoryId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
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

                // Enable the subcategory select element after data is fetched
                subcategorySelect.disabled = false;
                console.log('Subcategory select element enabled');
            })
            .catch(error => {
                console.error('Error:', error);
                // Ensure the subcategory select element is enabled even if there's an error
                subcategorySelect.disabled = false;
                console.log('Subcategory select element enabled after error');
            });
    });
});

