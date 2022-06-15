/**Gives the ability to add additional questions. */

const addAnotherBtn = document.querySelector("#add-another");

/**
 * Update the total number of forms in the formset management data.
 * @param {HTMLFormElement} form - The target form containing the formset.
 * @param {Number} numForms - The new value for the total number of forms.
 */
const updateTotalForms = (form, numForms) => {
  form.querySelector("[name='form-TOTAL_FORMS']").value = numForms;
};

/**
 * Get the total number of forms in the formset management data.
 * @param {HTMLFormElement} form - The target form containing the formset.
 * @returns {Number} The total number of forms.
 */
const getTotalForms = (form) => {
  return parseInt(form.querySelector("[name='form-TOTAL_FORMS']").value);
};

const createNewForm = (form) => {
  const numForms = getTotalForms(form);
  updateTotalForms(form, numForms + 1);
  // Form num in the element starts at index 0.
  const new_html = _newFormHtml(form, numForms);
  // Add the new html before the add another button.
  addAnotherBtn.insertAdjacentHTML("beforebegin", new_html);
};

const _newFormHtml = (form, numForms) => {
  const orig_html = form.querySelector(".forms__form").outerHTML;
  // Update the form number.
  let new_html = orig_html.replaceAll("-0-", `-${numForms}-`);
  // Remove old value
  console.log(new_html);
  new_html = new_html.replace(/(?<!<option )(value=")(.*?)(")/g, "$2$4");
  // Remove textarea value
  new_html = new_html.replace(/(<textarea.*?>)(.*?)(<)/g, "$1$3");
  // Remove the element containing the form id by removing the name field.
  new_html = new_html.replace(`name="form-${numForms}-id"`, "");

  return new_html;
};

const main = () => {
  addAnotherBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createNewForm(document.querySelector("form"));
  });
};

main();
