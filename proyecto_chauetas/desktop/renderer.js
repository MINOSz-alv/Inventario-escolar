const API_BASE = 'http://127.0.0.1:8000/api';
const { useState, useEffect } = React;
const root = ReactDOM.createRoot(document.getElementById('root'));

function ItemCard({ item }) {
  return React.createElement(
    'div',
    { className: 'item-card' },
    React.createElement('div', { className: 'item-name' }, item.name),
    React.createElement('div', { className: 'item-quantity' }, item.quantity)
  );
}

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState('1');
  const [status, setStatus] = useState({ text: 'Abre la app y conecta con el backend local.', isError: false });

  useEffect(() => {
    fetchItems();
  }, []);

  function setError(message) {
    setStatus({ text: message, isError: true });
  }

  function fetchItems() {
    fetch(`${API_BASE}/items/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('No se pudo cargar el inventario.');
        }
        return res.json();
      })
      .then((data) => {
        setItems(data);
        setStatus({ text: 'Conectado. Inventario cargado.', isError: false });
      })
      .catch((error) => {
        console.error(error);
        setError('Error de conexión. Asegura el backend local en http://127.0.0.1:8000');
      });
  }

  function addItem() {
    const trimmedName = name.trim();
    const parsedQuantity = Number(quantity);

    if (!trimmedName || Number.isNaN(parsedQuantity) || parsedQuantity <= 0) {
      setError('Ingresa un nombre válido y una cantidad mayor a cero.');
      return;
    }

    fetch(`${API_BASE}/items/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: trimmedName, quantity: parsedQuantity }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Error al agregar elemento.');
        }
        return res.json();
      })
      .then(() => {
        setName('');
        setQuantity('1');
        fetchItems();
      })
      .catch((error) => {
        console.error(error);
        setError('No se pudo agregar el ítem. Verifica el backend.');
      });
  }

  return React.createElement(
    'div',
    { className: 'app-shell' },
    React.createElement(
      'header',
      null,
      React.createElement(
        'div',
        null,
        React.createElement('h1', null, 'Inventario Escolar'),
        React.createElement('p', null, 'App local de escritorio')
      ),
      React.createElement('div', { className: `status ${status.isError ? 'status-error' : ''}` }, status.text)
    ),
    React.createElement(
      'main',
      null,
      React.createElement(
        'section',
        { className: 'card' },
        React.createElement(
          'div',
          { className: 'dashboard-header' },
          React.createElement(
            'div',
            null,
            React.createElement('h2', null, 'Inventario'),
            React.createElement('p', null, 'Acceso local sin autenticación.')
          )
        ),
        React.createElement(
          'section',
          { className: 'card' },
          React.createElement('h3', null, 'Agregar nuevo artículo'),
          React.createElement(
            'div',
            { className: 'field' },
            React.createElement('label', { htmlFor: 'item-name' }, 'Nombre'),
            React.createElement('input', {
              id: 'item-name',
              type: 'text',
              value: name,
              onChange: (event) => setName(event.target.value),
            })
          ),
          React.createElement(
            'div',
            { className: 'field' },
            React.createElement('label', { htmlFor: 'item-quantity' }, 'Cantidad'),
            React.createElement('input', {
              id: 'item-quantity',
              type: 'number',
              min: '1',
              value: quantity,
              onChange: (event) => setQuantity(event.target.value),
            })
          ),
          React.createElement('button', { onClick: addItem }, 'Agregar ítem')
        ),
        React.createElement(
          'section',
          { className: 'card' },
          React.createElement('h3', null, 'Lista de ítems'),
          React.createElement(
            'div',
            { className: 'items-list' },
            items.length === 0
              ? React.createElement('div', { className: 'empty-state' }, 'No hay ítems registrados aún.')
              : items.map((item) => React.createElement(ItemCard, { key: item.id, item }))
          )
        )
      )
    )
  );
}

root.render(React.createElement(App));
