const baseUrl = 'http://127.0.0.1:5000/api/items';

// 🚀 Add new item
function addItem() {
  const data = {
    name: document.getElementById('name').value,
    quantity: parseInt(document.getElementById('quantity').value),
    price: parseFloat(document.getElementById('price').value),
    category: document.getElementById('category').value
  };

  if (!data.name || isNaN(data.quantity) || isNaN(data.price) || !data.category) {
    alert("Please fill all fields correctly.");
    return;
  }

  fetch(baseUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(() => {
    alert("✅ Item added!");
    clearInputs();
    getAllItems();
  });
}

// 🔄 Get all items
function getAllItems() {
  fetch(baseUrl)
    .then(res => res.json())
    .then(items => renderTable(items));
}

// ❌ Get out-of-stock items
function getOutOfStock() {
  fetch(`${baseUrl}/out-of-stock`)
    .then(res => res.json())
    .then(items => renderTable(items));
}

// 🔍 Search items
function searchItems() {
  const query = document.getElementById('searchBox').value.trim();
  if (!query) {
    alert("Please enter a search term.");
    return;
  }

  fetch(`${baseUrl}/search?q=${encodeURIComponent(query)}`)
    .then(res => res.json())
    .then(items => {
      if (items.length === 0) {
        alert("No items found.");
      }
      renderTable(items);
    })
    .catch(error => {
      console.error('Search failed:', error);
      alert("Something went wrong during search.");
    });
}

// 🧾 Render table with editable rows
function renderTable(items) {
  const tbody = document.querySelector('#itemsTable tbody');
  tbody.innerHTML = '';
  items.forEach(item => {
    tbody.innerHTML += `
      <tr>
        <td>${item.id}</td>
        <td><input id="name-${item.id}" value="${item.name}"></td>
        <td><input id="qty-${item.id}" type="number" value="${item.quantity}"></td>
        <td><input id="price-${item.id}" type="number" value="${item.price}"></td>
        <td><input id="cat-${item.id}" value="${item.category}"></td>
        <td>${item.quantity > 0 ? '✅' : '❌'}</td>
        <td>
          <button class="btn-add" onclick="updateItem(${item.id})">💾 Save</button>
          <button class="btn-danger" onclick="deleteItem(${item.id})">🗑️</button>
        </td>
      </tr>
    `;
  });
}

// 💾 Update item
function updateItem(id) {
  const data = {
    name: document.getElementById(`name-${id}`).value,
    quantity: parseInt(document.getElementById(`qty-${id}`).value),
    price: parseFloat(document.getElementById(`price-${id}`).value),
    category: document.getElementById(`cat-${id}`).value,
    in_stock: parseInt(document.getElementById(`qty-${id}`).value) > 0
  };

  fetch(`${baseUrl}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(() => {
    alert("✅ Item updated!");
    getAllItems();
  });
}

// 🗑️ Delete item
function deleteItem(id) {
  if (confirm("Are you sure you want to delete this item?")) {
    fetch(`${baseUrl}/${id}`, {
      method: 'DELETE'
    })
    .then(res => res.json())
    .then(() => {
      alert("🗑️ Item deleted.");
      getAllItems();
    });
  }
}

// 🔄 Clear input fields after adding
function clearInputs() {
  document.getElementById('name').value = '';
  document.getElementById('quantity').value = '';
  document.getElementById('price').value = '';
  document.getElementById('category').value = '';
}
