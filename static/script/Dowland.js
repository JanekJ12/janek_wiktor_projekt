document.addEventListener('DOMContentLoaded', () => {
  // Obsługa menu mobilnego
  const toggleBtn = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.menu');

  toggleBtn.addEventListener('click', () => {
    menu.classList.toggle('open');
  });

  // Ładowanie plików z folderu image_Drop
  fetch('/list-files')
    .then(res => res.json())
    .then(files => {
      const container = document.getElementById('fileList');
      if (!container) return; // np. na innych stronach

      if (!Array.isArray(files) || files.length === 0) {
        container.innerHTML = '<p>Brak plików do pobrania.</p>';
        return;
      }

      files.forEach(file => {
        const fileCard = document.createElement('div');
        fileCard.className = 'file-item';

        const image = document.createElement('img');
        image.src = `/static/image_Drop/${encodeURIComponent(file)}`;
        image.alt = file;

        const info = document.createElement('div');
        info.className = 'file-info';

        const name = document.createElement('p');
        name.textContent = file;

        const downloadLink = document.createElement('a');
        downloadLink.href = `/download/${encodeURIComponent(file)}`;
        downloadLink.textContent = 'Pobierz';
        downloadLink.setAttribute('download', file);

        info.appendChild(name);
        info.appendChild(downloadLink);
        fileCard.appendChild(image);
        fileCard.appendChild(info);
        container.appendChild(fileCard);
      });
    })
    .catch(err => {
      console.error('Błąd:', err);
      const container = document.getElementById('fileList');
      if (container) {
        container.innerHTML = '<p>Nie udało się pobrać listy plików.</p>';
      }
    });
});
