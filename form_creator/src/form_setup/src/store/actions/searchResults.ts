import { AnyPropsObj } from "../../interfaces";
import * as actionTypes from "./actionTypes";


/**
 * Action to update the form.
 * @param formFields The form fields to update.
 */
export const updateForm = (formFields: AnyPropsObj) => {
  return {
    type: actionTypes.UPDATE_FORM,
    formFields,
  };
}
