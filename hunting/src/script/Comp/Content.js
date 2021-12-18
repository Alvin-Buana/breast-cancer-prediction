class Content extends HTMLElement {
  set place(data) {
    this._place = data;
    console.log(data);
    this.render();
  }

  render() {
    this.innerHTML = `
      <div class="col-sm-4">
        <div class="card" style="width: 25rem;box-shadow: 10px 10px 5px grey; margin-bottom :10px;">
          <img src="${this._place.Link}" class="card-img-top" alt="${this._place.Place_Name}" style = "width: 24.9rem; height : 18rem;">
            <div class="card-body">
              <h5 class="card-title" >${this._place.Place_Name}</h5>
                <p class="card-text">${
                  this._place.Category ? this._place.Category : "-"
                }</p>
                <a href="#" class="btn  btn-success">Go to Detail</a>
              </div>
          </div>
      </div>`;
  }
}
customElements.define("c-content", Content);
