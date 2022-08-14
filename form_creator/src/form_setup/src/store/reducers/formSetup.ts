// import {updateObject} from "../../utils";
import { Form, HTMLComponent, FormQuestion, ElementType, ReducerAction } from "../../interfaces";
import { updateObject } from "../../utils";
import * as actionTypes from "../actions/actionTypes";

export interface State {
  form: Form,
  formElements: {
    element: HTMLComponent | FormQuestion,
    elementType: ElementType,
  }[],
  meta: {
    maxSeqNo: number,
  }
}
const initialState: State = {
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
}


const updateForm = (state: State, action: ReducerAction) => {
  return updateObject(state, {
    form: updateObject(state.form, action.formFields),
  });
}

const reducer = (state: State = initialState, action: ReducerAction) => {
  switch (action.type) {
    case actionTypes.UPDATE_FORM:
      return updateForm(state, action) as State;
    default:
      return state;
  }
}

export default reducer;