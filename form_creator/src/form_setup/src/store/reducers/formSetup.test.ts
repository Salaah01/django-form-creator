import reducer, { State } from "./formSetup";
import * as actionTypes from "../actions/actionTypes";

describe("UPDATE_FORM", () => {
  const formFields = {
    title: "test",
    startDt: "2020-01-01",
    endDt: "2020-01-02",
    status: "draft",
  };
  const action = {
    type: actionTypes.UPDATE_FORM,
    formFields,
  };

  const state = {
    form: { title: "", startDt: "", endDt: "", status: "", },
    meta: { maxSeqNo: 10 }
  } as State;
  const updatedState = reducer(state, action);

  it("should update the form.", () => {
    expect(updatedState.form.title).toBe("test");
    expect(updatedState.form.startDt).toBe("2020-01-01");
    expect(updatedState.form.endDt).toBe("2020-01-02");
    expect(updatedState.form.status).toBe("draft");
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      form: { title: "", startDt: "", endDt: "", status: "", },
      meta: { maxSeqNo: 10 }
    });
  })

})