// import {updateObject} from "../../utils";
import { Form, ReducerAction, FormElement } from "../../interfaces";
import { updateObject } from "../../utils";
import * as actionTypes from "../actions/actionTypes";
import * as screens from "../../screens";
export interface State {
  screen: screens.ScreenOption,
  form: Form,
  formElements: FormElement[],
  meta: {
    maxSeqNo: number,
  }
}
const initialState: State = {
  screen: screens.FORM_DETAILS,
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