import {
  AnyPropsObj,
  ElementType,
  FormDetail,
  FormElement,
  HttpMethod,
} from "../../interfaces";
import { ScreenOption } from "../../screens";
import * as actionTypes from "./actionTypes";

/**
 * Updates the HTTP method to use.
 * @param httpMethod - The HTTP method to use.
 */
export const updateHTTPMethod = (httpMethod: HttpMethod) => {
  return {
    type: actionTypes.UPDATE_HTTP_METHOD,
    httpMethod,
  };
};

/**
 * Action to update the form.
 * @param formFields - The form fields to update.
 */
export const updateForm = (formFields: AnyPropsObj) => {
  return {
    type: actionTypes.UPDATE_FORM,
    formFields,
  };
};

/**
 * Action to add a form element.
 * @param formElement - The form element to add.
 */
export const addFormElement = (formElement: FormElement) => {
  return {
    type: actionTypes.ADD_FORM_ELEMENT,
    formElement,
  };
};

/**
 * Action to update the form elements.
 * @param id - The id of the form element to update.
 * @param formElement - The form element to update.
 */
export const updateFormElement = (id: number, formElement: FormElement) => {
  return {
    type: actionTypes.UPDATE_FORM_ELEMENT,
    id: id,
    formElement,
  };
};

/**
 * Action to delete a form element.
 * @param id - The id of the form element to delete.
 */
export const deleteFormElement = (id: number) => {
  return {
    type: actionTypes.DELETE_FORM_ELEMENT,
    id: id,
  };
};

/**
 * Updates all form details including form elements.
 * @param formDetails - The form details to update.
 */
export const updateFormDetails = (formDetails: FormDetail) => {
  return {
    type: actionTypes.UPDATE_FORM_DETAILS,
    formDetails,
  };
};

/**
 * Updates the current screen to use.
 * @param screen - The screen to use.
 */
export const updateScreen = (screen: ScreenOption) => {
  return {
    type: actionTypes.UPDATE_SCREEN,
    screen,
  };
};

/**
 * Adds a blank form element.
 * @param elementType - The type of element to add.
 * @param formID - The id of the form to add the element to.
 */
export const addBlankFormElement = (
  elementType: ElementType,
  formID: Number
) => {
  return {
    type: actionTypes.ADD_BLANK_FORM_ELEMENT,
    elementType,
    formID,
  };
};
