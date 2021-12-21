class Content extends HTMLElement {
  set place(data) {
    this._place = data;
    console.log(data);
    this.render();
  }

  render() {
    this.setAttribute('class', 'col col-sm-4 col-xs-6');
    this.innerHTML = `
        <div class="card" style="width: 25rem; margin-bottom :10px;">
          <img src="${this._place.Link}" class="card-img-top" alt="${this._place.Place_Name}" style = "width: 24.9rem; height : 18rem;">
            <div class="card-body">
              <h5 class="card-title" >${this._place.Place_Name}</h5>
                <p class="card-text">${this._place.Category ? this._place.Category : '-'}</p>
                <a href="../../../../found/index.html" class="btn  btn-success">Go to Detail</a>
              </div>
          </div>`;
    this.addEventListener('click', (event) => {
      localStorage.setItem('place', JSON.stringify(this._place));
      let test = localStorage.getItem('place');
      console.log(test);
    });
  }
}
customElements.define('c-content', Content);
