// Inicializa Signature Pad
const canvas = document.getElementById('signature-pad');
const signaturePad = new SignaturePad(canvas);
console.log("SignaturePad inicializado:", signaturePad);

// Botón para borrar la firma
document.getElementById('signature-form').addEventListener('submit', async (event) => {
  event.preventDefault();

  const form = document.getElementById('signature-form');
  const formData = new FormData(form);

  // Agregar la firma al FormData
  const canvas = document.getElementById('signature-pad');
  const signaturePad = new SignaturePad(canvas);
  if (signaturePad.isEmpty()) {
    alert('Por favor, añade tu firma.');
    return;
  }

  const signature = signaturePad.toDataURL();
  formData.append('signature', signature);

  try {
    const response = await fetch('/guardar', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    if (result.status === 'success') {
      alert('Datos enviados correctamente.');
    } else {
      throw new Error(result.message);
    }
  } catch (error) {
    console.error('Error al enviar el formulario:', error);
    alert('Error al enviar el formulario.');
  }
});
