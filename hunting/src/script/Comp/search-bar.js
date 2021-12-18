class SearchBar extends HTMLElement {
  constructor() {
    super();
    this.shadowDOM = this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  set clickEvent(event) {
    this._clickEvent = event;
    this.render();
  }

  get value() {
    return this.shadowDOM.querySelector('#searchElement').value;
  }

  render() {
    this.shadowDOM.innerHTML = `
      <link rel="stylesheet" href="./src/style/style.css" />
     
      <div class="sticky-bg ">
        <a  class="backbutton" href="../index.html">Beranda</a>
        
      <div id="search-container" class="search-container">
           <input placeholder="Search Place" id="searchElement" type="search">
           <button id="searchButtonElement" type="submit">Search</button>
       </div>
       </div>
       `;

    this.shadowDOM.querySelector('#searchButtonElement').addEventListener('click', this._clickEvent);
  }
}

customElements.define('search-bar', SearchBar);
