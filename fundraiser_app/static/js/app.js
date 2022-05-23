document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
    class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

  // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;
      console.log(this.currentStep)
      // TODO: get data from inputs and show them in summary
      //selected categories

      if (this.currentStep == 5) {
        let input_categories = [...document.querySelectorAll(".input_categories")].filter(el => el.checked === true);
        const input_categories_id = [];
        const input_categories_names = [];
        input_categories.forEach(el => {
          input_categories_id.push(parseInt(el.value));
          input_categories_names.push(el.parentElement.children[2].innerText);
        })
        console.log(input_categories);
        console.log(input_categories_id);
        console.log(input_categories_names)

        let input_bags = parseInt(document.querySelector(".input-bags").value);

        let input_organization = [...document.querySelectorAll(".input_organization")].filter(el => el.checked === true)[0]
        const input_organization_id = parseInt(input_organization.value);
        const input_organization_name = input_organization.parentElement.children[2].children[0].innerText

        console.log(input_bags)
        console.log(input_organization);
        console.log(input_organization_id);
        console.log(input_organization_name);

        const street = document.querySelector("#street").value;
        const city = document.querySelector("#city").value;
        const postcode = document.querySelector("#postcode").value;
        const phone = document.querySelector("#phone").value;
        const date = document.querySelector("#date").value;
        const time = document.querySelector("#time").value;
        const more_info = document.querySelector("#more_info").value;


        document.querySelector("#summary-bags-category").innerText = input_categories_names;
        document.querySelector("#summary-organization").innerText = input_organization_name
        const summary_adress = document.querySelector("#summary-adress").children
        const summary_term = document.querySelector("#summary-term").children
        summary_adress[0].innerText = street
        summary_adress[1].innerText = city
        summary_adress[2].innerText = postcode
        summary_adress[3].innerText = phone
        summary_term[0].innerText = date
        summary_term[1].innerText = time
        summary_term[2].innerText = more_info

      }
    }
    /**
     * Submit form
     *
     *


     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();


        let input_categories = [...document.querySelectorAll(".input_categories")].filter(el => el.checked === true);
        const input_categories_id = [];
        input_categories.forEach(el => {
          input_categories_id.push(parseInt(el.value));
        })
        let input_organization = [...document.querySelectorAll(".input_organization")].filter(el => el.checked === true)[0]
        const input_organization_id = parseInt(input_organization.value)


        let input_bags = parseInt(document.querySelector(".input-bags").value);
        const street = document.querySelector("#street").value;
        const city = document.querySelector("#city").value;
        const postcode = document.querySelector("#postcode").value;
        const phone = document.querySelector("#phone").value;
        const date = document.querySelector("#date").value;
        const time = document.querySelector("#time").value;
        const more_info = document.querySelector("#more_info").value;

      // const formularz = document.querySelector('#form')
      // const data = new FormData(formularz)
      // data.append("categories", input_categories_id);
      // data.append("institution", input_organization_id);
      // data.append("quantity", input_bags);
      // data.append("address_street_no", street);
      // data.append("city", city);
      // data.append("zip_code", postcode);
      // data.append("phone", phone);
      // data.append("pick_up_date", date);
      // data.append("pick_up_time", time);
      // data.append("pick_up_comment", more_info);

      // console.log(data);
    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

 const formularz = document.querySelector('#form')
const data = new FormData(formularz)
      fetch('/add_donation/', {
        method: 'POST',
        redirect: "follow",
        credentials: "same-origin",
        headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json"
    },
        body: data,
      })
      .then(response => response.json())
      .then(data => {
            window.location.href = '/form_confirmation/';
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
