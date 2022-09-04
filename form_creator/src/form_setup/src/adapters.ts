/**This modules contains adapters for transforming objects from the state they
 * arrive in via the API to a form that can be used by this application.
 */

import {
  APIElementType,
  APIFormDetail,
  APIFormElement,
  APIFormQuestion,
  APIHTMLComponent,
  ElementType,
  FormDetail,
  FormElement,
  FormQuestion,
  HTMLComponent,
} from "./interfaces";

/**
 * Converts an API form element to a form element.
 * @param data - The API form element.
 * @returns - The form element.
 */
export const formDetailFromAPI = (data: APIFormDetail): FormDetail => {
  return {
    form: {
      id: data.id,
      title: data.title,
      slug: data.slug,
      description: data.description || "",
      startDt: data.start_dt,
      endDt: data.end_dt || "",
      status: data.status,
    },
    formElements: data.form_elements.map((element) => {
      return formElementFromAPI(element);
    }),
  };
};

/**
 * Converts the form detail data to a format acceptable by the API.
 * @param data - The form detail data.
 */
export const formDetailToAPI = (data: FormDetail): APIFormDetail => {
  const formDetail: APIFormDetail = {
    title: data.form.title,
    slug: data.form.slug || "",
    description: data.form.description || null,
    start_dt: data.form.startDt || "",
    end_dt: data.form.endDt || "",
    status: data.form.status || "",
    form_elements: data.formElements.map((element) => {
      return formElementToAPI(element);
    }),
  };

  if (data.form.id) {
    formDetail.id = data.form.id;
  }

  return formDetail;
};

/**
 * Converts the `element_type` field from the API to an element type.
 * @param data - The API element type.
 * @returns  - The element type.
 */
const elementTypeFromAPI = (data: APIElementType): ElementType => {
  return {
    id: data.id,
    appLabel: data.app_label,
    model: data.model,
  };
};

/**
 * Converts the element type data to a format acceptable by the API.
 * @param data - The element type data.
 * @returns
 */
const elementTypeToAPI = (data: ElementType): APIElementType => {
  return {
    app_label: data.appLabel!,
    model: data.model!,
  };
};

/**
 * Converts an API HTML component to an HTML component.
 * @param data - The API HTML component.
 * @returns - The HTML component.
 */
export const HTMLComponentFromAPI = (data: APIHTMLComponent): HTMLComponent => {
  return {
    id: data.id,
    form: data.form,
    seqNo: data.seq_no,
    html: data.html,
  };
};

/**
 * Converts a HTML component element to a format acceptable by the API.
 * @param data - The HTML component element.
 */
const HTMLComponentToAPI = (data: HTMLComponent): APIHTMLComponent => {
  if (!data.form) {
    throw new Error("Form is required.");
  }
  
  const apiData: APIHTMLComponent = {
    html: data.html,
    form: data.form,
  };
  if (data.id) {
    apiData.id = data.id;
  }
  if (data.seqNo) {
    apiData.seq_no = data.seqNo;
  }
  return apiData;
};

/**
 * Converts an API form question to a form question.
 * @param data - The API form question.
 * @returns - The form question.
 */
export const formQuestionFromAPI = (data: APIFormQuestion): FormQuestion => {
  return {
    id: data.id,
    form: data.form,
    seqNo: data.seq_no,
    fieldType: data.field_type,
    question: data.question,
    description: data.description,
    required: data.required,
    choices: data.choices.split("|"),
    relatedQuestion: data.related_question,
  };
};

/**
 * Converts a form question to a format acceptable by the API.
 * @param data - The form question.
 */
const formQuestionToAPI = (data: FormQuestion): APIFormQuestion => {
  if (!data.form) {
    throw new Error("Form is required.");
  }

  const apiData: APIFormQuestion = {
    form: data.form,
    field_type: data.fieldType,
    question: data.question,
    description: data.description,
    required: data.required,
    choices: (data.choices || []).join("|"),
  };

  if (data.id) {
    apiData.id = data.id;
  }
  if (data.seqNo) {
    apiData.seq_no = data.seqNo;
  }
  if (data.relatedQuestion) {
    apiData.related_question = data.relatedQuestion;
  }

  return apiData;
};

/**
 * Converts an API form element to a form element.
 * @param data - The API form element.
 * @returns - The form element.
 */
export const formElementFromAPI = (data: APIFormElement): FormElement => {
  const elementType = elementTypeFromAPI(data.element_type);
  const model = elementType.model;

  let element: HTMLComponent | FormQuestion;
  switch (model) {
    case "htmlcomponent":
      element = HTMLComponentFromAPI(data.element as APIHTMLComponent);
      break;
    case "formquestion":
      element = formQuestionFromAPI(data.element as APIFormQuestion);
      break;
    default:
      throw new Error(`Unknown element type: ${model}`);
  }

  return {
    element: element,
    elementType: elementType,
  };
};

export const formElementToAPI = (data: FormElement): APIFormElement => {
  const elementType = elementTypeToAPI(data.elementType);
  const model = elementType.model;

  let element: APIHTMLComponent | APIFormQuestion;
  switch (model) {
    case "htmlcomponent":
      element = HTMLComponentToAPI(data.element as HTMLComponent);
      break;
    case "formquestion":
      element = formQuestionToAPI(data.element as FormQuestion);
      break;
    default:
      throw new Error(`Unknown element type: ${model}`);
  }

  const apiData: APIFormElement = {
    element_type: elementType,
    element: element,
    form: element.form,
  };
  if (element.id) {
    apiData.id = element.id;
  }
  if (element.seq_no) {
    apiData.seq_no = element.seq_no;
  }

  return apiData;
};
