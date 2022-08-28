// import {updateObject} from "../../utils";
import {
  FormDetail,
  ReducerAction,
  FormElement,
  HttpMethod,
  Form,
} from "../../interfaces";
import { updateObject } from "../../utils";
import * as actionTypes from "../actions/actionTypes";
import * as screens from "../../screens";

export interface State extends FormDetail {
  screen: screens.ScreenOption;
  httpMethod: HttpMethod;
  meta: {
    maxSeqNo: number;
  };
}

const initialState: State = {
  screen: screens.FORM_DETAILS,
  httpMethod: "POST",
  form: {
    editorOptions: [],
    editors: [],
    title: "",
    description: "",
    startDt: "",
    endDt: "",
    status: "",
  },
  formElements: [],
  meta: {
    maxSeqNo: 0,
  },
};

/**
 * Updates the HTTP method to use.
 * @param action.httpMethod - The HTTP method to use.
 */
const updateHTTPMethod = (
  state: State,
  action: { httpMethod: HttpMethod }
): State => {
  return updateObject(state, { httpMethod: action.httpMethod }) as State;
};

/**Updates the form details with data from new fields. */
const updateForm = (state: State, action: ReducerAction): State => {
  return updateObject(state, {
    form: updateObject(state.form, action.formFields),
  }) as State;
};

/**
 * Adds a new form element.
 * @param action.formElement - The form element to add.
 */
const addFormElement = (
  state: State,
  action: { formElement: FormElement }
): State => {
  return updateObject(state, {
    formElements: [...state.formElements, action.formElement],
  }) as State;
};

/**
 * Updates the form element with new data.
 * @param action.id - The id of the form element to update.
 * @param action.formElement - Object containing the new data.
 */
const updateFormElement = (
  state: State,
  action: { id: number; formElement: FormElement }
): State => {
  // Find index of form element to update.
  const index = state.formElements.findIndex(
    (fe) => fe.element.id === action.id
  );
  // If found, update the form element.
  if (index !== -1) {
    return updateObject(state, {
      formElements: [
        ...state.formElements.slice(0, index),
        action.formElement,
        ...state.formElements.slice(index + 1),
      ],
    }) as State;
  } else {
    return state;
  }
};

/**
 * Deletes a form element.
 * @param action.id - The id of the form element to delete.
 */
const deleteFormElement = (state: State, action: { id: number }): State => {
  // Find index of form element to delete.
  const index = state.formElements.findIndex(
    (fe) => fe.element.id === action.id
  );
  // If found, delete the form element.
  if (index !== -1) {
    return updateObject(state, {
      formElements: [
        ...state.formElements.slice(0, index),
        ...state.formElements.slice(index + 1),
      ],
    }) as State;
  } else {
    return state;
  }
};

/**
 * Updates the state with new form data. This process improves the full
 * replacement of the form data.
 * @param action.form - The new form data.
 * @param action.formElements - The new form elements.
 */
const updateFormDetails = (
  state: State,
  action: {
    id: number;
    formDetails: { form: Form; formElements: FormElement[] };
  }
): State => {
  return updateObject(state, {
    form: action.formDetails.form,
    formElements: action.formDetails.formElements,
  }) as State;
};

/**
 * Updates the current screen to use.
 * @param action.screen - The screen to use.
 */
const updateScreen = (
  state: State,
  action: { screen: screens.ScreenOption }
): State => {
  return updateObject(state, {
    screen: action.screen,
  }) as State;
};

const reducer = (state: State = initialState, action: ReducerAction) => {
  switch (action.type) {
    case actionTypes.UPDATE_HTTP_METHOD:
      return updateHTTPMethod(
        state,
        action as unknown as { httpMethod: HttpMethod }
      );

    case actionTypes.UPDATE_FORM:
      return updateForm(state, action);

    case actionTypes.ADD_FORM_ELEMENT:
      return addFormElement(
        state,
        action as unknown as { formElement: FormElement }
      );

    case actionTypes.UPDATE_FORM_ELEMENT:
      return updateFormElement(
        state,
        action as unknown as { id: number; formElement: FormElement }
      );

    case actionTypes.DELETE_FORM_ELEMENT:
      return deleteFormElement(state, action as unknown as { id: number });

    case actionTypes.UPDATE_FORM_DETAILS:
      return updateFormDetails(
        state,
        action as unknown as {
          id: number;
          formDetails: { form: Form; formElements: FormElement[] };
        }
      );

    case actionTypes.UPDATE_SCREEN:
      return updateScreen(
        state,
        action as unknown as { screen: screens.ScreenOption }
      );

    default:
      return state;
  }
};

export default reducer;
