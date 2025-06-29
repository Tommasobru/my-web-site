async function loadProjects() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/projects');
      const data = await response.json();         // <-- qui ricevi l'oggetto { projects: [...] }
      const projects = data.projects;             // <-- accedi all'array vero
  
      const carousel = document.getElementById('projects-carousel');
  
      projects.forEach(project => {
        const card = document.createElement('div');
        card.className = 'card';
  
        card.innerHTML = `
          <img src="${project.image}" alt="${project.name}" style="width:100%; border-radius:10px;">
          <h3>${project.name}</h3>
          <p>${project.description || 'Nessuna descrizione disponibile.'}</p>
          <a href="${project.url}" target="_blank">Vai al progetto</a>
        `;
  
        carousel.appendChild(card);
      });
    } catch (error) {
      console.error('Errore durante il caricamento dei progetti:', error);
    }
  }
  

document.addEventListener('DOMContentLoaded', loadProjects);