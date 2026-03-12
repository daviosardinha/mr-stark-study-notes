// Certificate Lightbox
(function() {
  'use strict';

  // Create lightbox elements
  const lightbox = document.createElement('div');
  lightbox.id = 'cert-lightbox';
  lightbox.className = 'cert-lightbox';
  lightbox.innerHTML = `
    <div class="lightbox-overlay"></div>
    <div class="lightbox-container">
      <button class="lightbox-close" aria-label="Close">&times;</button>
      <button class="lightbox-nav lightbox-prev" aria-label="Previous">&#8249;</button>
      <button class="lightbox-nav lightbox-next" aria-label="Next">&#8250;</button>
      <div class="lightbox-content">
        <img class="lightbox-img" src="" alt="Certificate">
        <div class="lightbox-info">
          <h3 class="lightbox-title"></h3>
          <p class="lightbox-meta"></p>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(lightbox);

  // Get all certificate cards
  const certCards = document.querySelectorAll('.cert-card');
  let currentIndex = 0;
  const certData = Array.from(certCards).map(card => ({
    img: card.dataset.img,
    title: card.dataset.title,
    issuer: card.dataset.issuer,
    date: card.dataset.date
  }));

  // Open lightbox
  function openLightbox(index) {
    currentIndex = index;
    updateLightbox();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  // Close lightbox
  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Update lightbox content
  function updateLightbox() {
    const cert = certData[currentIndex];
    const img = lightbox.querySelector('.lightbox-img');
    const title = lightbox.querySelector('.lightbox-title');
    const meta = lightbox.querySelector('.lightbox-meta');
    
    img.src = cert.img;
    img.alt = cert.title;
    title.textContent = cert.title;
    
    const dateStr = cert.date ? new Date(cert.date).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long' 
    }) : 'Date unknown';
    meta.textContent = `${cert.issuer} • ${dateStr}`;
    
    // Update nav buttons
    lightbox.querySelector('.lightbox-prev').style.display = 
      currentIndex > 0 ? 'block' : 'none';
    lightbox.querySelector('.lightbox-next').style.display = 
      currentIndex < certData.length - 1 ? 'block' : 'none';
  }

  // Navigate
  function prevImage() {
    if (currentIndex > 0) {
      currentIndex--;
      updateLightbox();
    }
  }

  function nextImage() {
    if (currentIndex < certData.length - 1) {
      currentIndex++;
      updateLightbox();
    }
  }

  // Event listeners
  certCards.forEach((card, index) => {
    card.addEventListener('click', () => openLightbox(index));
  });

  lightbox.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
  lightbox.querySelector('.lightbox-prev').addEventListener('click', prevImage);
  lightbox.querySelector('.lightbox-next').addEventListener('click', nextImage);
  lightbox.querySelector('.lightbox-overlay').addEventListener('click', closeLightbox);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    
    switch(e.key) {
      case 'Escape':
        closeLightbox();
        break;
      case 'ArrowLeft':
        prevImage();
        break;
      case 'ArrowRight':
        nextImage();
        break;
    }
  });
})();
