const form = document.getElementById('contact-form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  try {
    const response = await fetch('http://127.0.0.1:8000/api/contatti', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      alert('Messaggio inviato con successo!');
      form.reset();
    } else {
      const errorData = await response.json();
      alert('Errore nell\'invio: ' + (errorData.detail || 'Errore sconosciuto'));
    }
  } catch (error) {
    alert('Errore di rete o server: ' + error.message);
  }
});
