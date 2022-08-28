import reducer, { State } from "./formSetup";
import * as actionTypes from "../actions/actionTypes";
import * as screens from "../../screens";

describe("UPDATE_HTTP_METHOD", () => {
  const state = {
    age: 10,
    httpMethod: "GET",
  } as unknown as State;

  const action = {
    type: actionTypes.UPDATE_HTTP_METHOD,
    httpMethod: "PUT",
  };

  const updatedState = reducer(state, action);

  it("should update the http method.", () => {
    expect(updatedState).toEqual({
      age: 10,
      httpMethod: "PUT",
    });
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      age: 10,
      httpMethod: "GET",
    });
  });
});

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
    form: { title: "", startDt: "", endDt: "", status: "" },
    meta: { maxSeqNo: 10 },
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
      form: { title: "", startDt: "", endDt: "", status: "" },
      meta: { maxSeqNo: 10 },
    });
  });
});

describe("ADD_FORM_ELEMENT", () => {
  const state = {
    form: { title: "", startDt: "", endDt: "", status: "" },
    formElements: [
      {
        element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
    ],
  } as State;
  const action = {
    type: actionTypes.ADD_FORM_ELEMENT,
    formElement: {
      element: { id: 2, seqNo: 2, html: "<h1>Hello World</h1>" },
      elementType: {
        id: "2",
        appLabel: "form_creator_2",
        model: "htmlcomponent_2",
      },
    },
  };
  const updatedState = reducer(state, action);

  it("should add a form element.", () => {
    expect(updatedState.formElements.length).toBe(2);
    expect(updatedState.formElements[1].element.id).toBe(2);
    expect(updatedState.formElements[1].elementType.id).toBe("2");
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      form: { title: "", startDt: "", endDt: "", status: "" },
      formElements: [
        {
          element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
          elementType: {
            id: "1",
            appLabel: "form_creator",
            model: "htmlcomponent",
          },
        },
      ],
    });
  });
});

describe("UPDATE_FORM_ELEMENT", () => {
  const state = {
    form: { title: "", startDt: "", endDt: "", status: "" },
    formElements: [
      {
        element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
      {
        element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
        elementType: {
          id: "2",
          appLabel: "form_creator_2",
          model: "htmlcomponent_2",
        },
      },
    ],
  } as State;
  const action = {
    type: actionTypes.UPDATE_FORM_ELEMENT,
    id: 1,
    formElement: {
      element: { id: 1, seqNo: 10, html: "<h1>Hello World, Again!</h1>" },
      elementType: {
        id: "1",
        appLabel: "form_creator",
        model: "htmlcomponent",
      },
    },
  };
  const updatedState = reducer(state, action);

  it("should update the form element.", () => {
    expect(updatedState.formElements).toEqual([
      {
        element: { id: 1, seqNo: 10, html: "<h1>Hello World, Again!</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
      {
        element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
        elementType: {
          id: "2",
          appLabel: "form_creator_2",
          model: "htmlcomponent_2",
        },
      },
    ]);
  });

  it("should return the original state if the id does not exist.", () => {
    const action = {
      type: actionTypes.UPDATE_FORM_ELEMENT,
      id: 3,
      formElement: {
        element: { id: 3, seqNo: 10, html: "<h1>Hello World, Again!</h1>" },
        elementType: {
          id: "3",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
    };
    const updatedState = reducer(state, action);
    expect(updatedState).toEqual(state);
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      form: { title: "", startDt: "", endDt: "", status: "" },
      formElements: [
        {
          element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
          elementType: {
            id: "1",
            appLabel: "form_creator",
            model: "htmlcomponent",
          },
        },
        {
          element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
          elementType: {
            id: "2",
            appLabel: "form_creator_2",
            model: "htmlcomponent_2",
          },
        },
      ],
    });
  });
});

describe("DELETE_FORM_ELEMENT", () => {
  const state = {
    form: { title: "", startDt: "", endDt: "", status: "" },
    formElements: [
      {
        element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
      {
        element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
        elementType: {
          id: "2",
          appLabel: "form_creator_2",
          model: "htmlcomponent_2",
        },
      },
    ],
  } as State;
  const action = {
    type: actionTypes.DELETE_FORM_ELEMENT,
    id: 1,
  };
  const updatedState = reducer(state, action);

  it("should delete the form element.", () => {
    expect(updatedState.formElements).toEqual([
      {
        element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
        elementType: {
          id: "2",
          appLabel: "form_creator_2",
          model: "htmlcomponent_2",
        },
      },
    ]);
  });

  it("should return the original state if the id does not exist.", () => {
    const action = {
      type: actionTypes.DELETE_FORM_ELEMENT,
      id: 3,
    };
    const updatedState = reducer(state, action);
    expect(updatedState).toEqual(state);
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      form: { title: "", startDt: "", endDt: "", status: "" },
      formElements: [
        {
          element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
          elementType: {
            id: "1",
            appLabel: "form_creator",
            model: "htmlcomponent",
          },
        },
        {
          element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
          elementType: {
            id: "2",
            appLabel: "form_creator_2",
            model: "htmlcomponent_2",
          },
        },
      ],
    });
  });
});

describe("UPDATE_FORM_DETAILS", () => {
  const state = {
    form: { title: "", startDt: "", endDt: "", status: "" },
    formElements: [
      {
        element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
      {
        element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
        elementType: {
          id: "2",
          appLabel: "form_creator_2",
          model: "htmlcomponent_2",
        },
      },
    ],
  } as State;
  const action = {
    type: actionTypes.UPDATE_FORM_DETAILS,
    formDetails: {
      form: {
        title: "Hello World",
        startDt: "2020-01-01",
        endDt: "2020-01-02",
        status: "draft",
      },
      formElements: [
        {
          element: { id: 1, seqNo: 1, html: "<h1>Updated Hello World</h1>" },
          elementType: {
            id: "1",
            appLabel: "form_creator",
            model: "htmlcomponent",
          },
        },
      ],
    },
  };

  const updatedState = reducer(state, action);

  it("should update the form details.", () => {
    expect(updatedState.form).toEqual({
      title: "Hello World",
      startDt: "2020-01-01",
      endDt: "2020-01-02",
      status: "draft",
    });
  });

  it("should update the form elements.", () => {
    expect(updatedState.formElements).toEqual([
      {
        element: { id: 1, seqNo: 1, html: "<h1>Updated Hello World</h1>" },
        elementType: {
          id: "1",
          appLabel: "form_creator",
          model: "htmlcomponent",
        },
      },
    ]);
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      form: { title: "", startDt: "", endDt: "", status: "" },
      formElements: [
        {
          element: { id: 1, seqNo: 1, html: "<h1>Hello World</h1>" },
          elementType: {
            id: "1",
            appLabel: "form_creator",
            model: "htmlcomponent",
          },
        },
        {
          element: { id: 2, seqNo: 2, html: "<h2>Hello World</h2>" },
          elementType: {
            id: "2",
            appLabel: "form_creator_2",
            model: "htmlcomponent_2",
          },
        },
      ],
    });
  });
});

describe("UPDATE_SCREEN", () => {
  const state = {
    age: 10,
    httpMethod: "GET",
    screen: screens.FORM_DETAILS,
  } as unknown as State;
  const action = {
    type: actionTypes.UPDATE_SCREEN,
    screen: screens.FORM_ELEMENTS,
  };
  const updatedState = reducer(state, action);

  it("should update the screen.", () => {
    expect(updatedState.screen).toEqual(screens.FORM_ELEMENTS);
  });

  it("should not have mutated the original state", () => {
    expect(state).toEqual({
      age: 10,
      httpMethod: "GET",
      screen: screens.FORM_DETAILS,
    });
  });
});
