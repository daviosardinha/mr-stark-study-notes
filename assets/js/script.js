'use strict';

// Page navigation - put this FIRST to ensure it runs
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

if (navigationLinks.length > 0 && pages.length > 0) {
  for (let i = 0; i < navigationLinks.length; i++) {
    navigationLinks[i].addEventListener("click", function () {
      // Remove active from all nav links
      navigationLinks.forEach(link => link.classList.remove("active"));
      // Add active to clicked
      this.classList.add("active");
      // Hide all pages
      pages.forEach(page => page.classList.remove("active"));
      // Show matching page
      const pageName = this.innerHTML.toLowerCase().trim();
      for (let j = 0; j < pages.length; j++) {
        if (pageName === pages[j].dataset.page) {
          pages[j].classList.add("active");
          window.scrollTo(0, 0);
          break;
        }
      }
    });
  }
}

// element toggle function
const elementToggleFunc = function (elem) { elem.classList.toggle("active"); }

// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
if (sidebarBtn) {
  sidebarBtn.addEventListener("click", function () { elementToggleFunc(sidebar); });
}

// testimonials variables
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");

// modal variable
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");

// modal toggle function - with null checks
const testimonialsModalFunc = function () {
  if (modalContainer && overlay) {
    modalContainer.classList.toggle("active");
    overlay.classList.toggle("active");
  }
}

// add click event to all modal items - with null checks
if (testimonialsItem.length > 0 && modalImg && modalTitle && modalText) {
  for (let i = 0; i < testimonialsItem.length; i++) {
    testimonialsItem[i].addEventListener("click", function () {
      modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
      modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
      modalTitle.innerHTML = this.querySelector("[data-testimonials-title]").innerHTML;
      modalText.innerHTML = this.querySelector("[data-testimonials-text]").innerHTML;
      testimonialsModalFunc();
    });
  }
}

// add click event to modal close button - with null checks
if (modalCloseBtn) {
  modalCloseBtn.addEventListener("click", testimonialsModalFunc);
}
if (overlay) {
  overlay.addEventListener("click", testimonialsModalFunc);
}

// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-selecct-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

if (select) {
  select.addEventListener("click", function () { elementToggleFunc(this); });

  for (let i = 0; i < selectItems.length; i++) {
    selectItems[i].addEventListener("click", function () {
      let selectedValue = this.innerText.toLowerCase();
      selectValue.innerText = this.innerText;
      elementToggleFunc(select);
      filterFunc(selectedValue);
    });
  }
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {
  for (let i = 0; i < filterItems.length; i++) {
    if (selectedValue === "all") {
      filterItems[i].classList.add("active");
    } else if (selectedValue === filterItems[i].dataset.category) {
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].classList.remove("active");
    }
  }
}

// add event in all filter button items
if (filterBtn.length > 0) {
  for (let i = 0; i < filterBtn.length; i++) {
    filterBtn[i].addEventListener("click", function () {
      let selectedValue = this.innerText.toLowerCase();
      filterFunc(selectedValue);
    });
  }
}

// portfolio variables
const projectItem = document.querySelectorAll("[data-project-item]");
const gridItem = document.querySelectorAll("[data-grid-item]");

// portfolio modal variables
const portfolioModal = document.querySelector("[data-portfolio-modal-open]");
const portfolioModalClose = document.querySelector("[data-portfolio-modal-close]");

// portfolio modal function
const portfolioModalFunc = function () {
  if (portfolioModal) {
    portfolioModal.classList.toggle("active");
  }
  if (portfolioModalClose) {
    portfolioModalClose.classList.toggle("active");
  }
}

// add click event to portfolio modal
if (projectItem.length > 0) {
  for (let i = 0; i < projectItem.length; i++) {
    projectItem[i].addEventListener("click", function () {
      portfolioModalFunc();
    });
  }
}

// add click event to portfolio modal close
if (portfolioModalClose) {
  portfolioModalClose.addEventListener("click", function () {
    if (portfolioModal) portfolioModal.classList.toggle("active");
    this.classList.toggle("active");
  });
}

//-----------------------------------*\
// BACK TO TOP BUTTON
//-----------------------------------*

const backToTopBtn = document.createElement('button');
backToTopBtn.id = 'backToTop';
backToTopBtn.textContent = '↑';
backToTopBtn.title = 'Back to top';
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', function() {
  if (window.scrollY > 300) {
    backToTopBtn.style.display = 'block';
  } else {
    backToTopBtn.style.display = 'none';
  }
});

backToTopBtn.addEventListener('click', function() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

//-----------------------------------*\
// COPY BUTTON FOR CODE BLOCKS
//-----------------------------------*

function addCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre code, pre');
  
  codeBlocks.forEach(function(codeBlock) {
    let pre = codeBlock.tagName === 'PRE' ? codeBlock : codeBlock.parentElement;
    
    if (pre.parentElement.classList.contains('code-block')) {
      return;
    }
    
    const wrapper = document.createElement('div');
    wrapper.className = 'code-block';
    
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'Copy';
    
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(copyBtn);
    wrapper.appendChild(pre);
    
    copyBtn.addEventListener('click', function() {
      let text = codeBlock.textContent || codeBlock.innerText;
      
      navigator.clipboard.writeText(text).then(function() {
        copyBtn.textContent = 'Copied!';
        copyBtn.classList.add('copied');
        
        setTimeout(function() {
          copyBtn.textContent = 'Copy';
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy:', err);
        copyBtn.textContent = 'Error';
      });
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', addCopyButtons);
} else {
  addCopyButtons();
}

//-----------------------------------*\
// BREADCRUMB NAVIGATION
//-----------------------------------*

function addBreadcrumbs() {
  const path = window.location.pathname;
  const pathParts = path.split('/').filter(part => part);
  
  if (pathParts.length < 2) return;
  
  const breadcrumbs = document.createElement('div');
  breadcrumbs.className = 'breadcrumbs';
  
  let breadcrumbHTML = '<a href="/">Home</a>';
  
  let currentPath = '';
  const sectionNames = {
    'certifications': 'Certifications',
    'crtp': 'CRTP',
    'crte': 'CRTE',
    'goad': 'GOAD',
    'ctf': 'CTF',
    'netexec-labs': 'NetExec Labs'
  };
  
  for (let i = 0; i < pathParts.length; i++) {
    const part = pathParts[i];
    currentPath += '/' + part;
    
    let name = part.replace('.html', '').replace(/-/g, ' ');
    
    if (sectionNames[part]) {
      name = sectionNames[part];
    } else if (part.startsWith('part-')) {
      const num = part.replace('part-', '').replace('.html', '');
      const titleMatch = document.querySelector('title');
      if (titleMatch) {
        name = titleMatch.textContent.split(' - ')[0].trim();
      } else {
        name = 'Part ' + num;
      }
    }
    
    if (i === pathParts.length - 1) {
      breadcrumbHTML += '<span>›</span><span class="current-page">' + name + '</span>';
    } else {
      breadcrumbHTML += '<span>›</span><a href="' + currentPath + '">' + name + '</a>';
    }
  }
  
  breadcrumbs.innerHTML = breadcrumbHTML;
  
  const article = document.querySelector('article');
  if (article) {
    article.insertBefore(breadcrumbs, article.firstChild);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', addBreadcrumbs);
} else {
  addBreadcrumbs();
}
