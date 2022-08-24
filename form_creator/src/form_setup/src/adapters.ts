/**This modules contains adapters for transforming objects from the state they
 * arrive in via the API to a form that can be used by this application.
 */

import {
  ElementType,
  FormDetail,
  FormElement,
  FormQuestion,
  HTMLComponent,
} from "./interfaces";

/**Interface for the form details part of an API. */
interface APIForm {
  id: number;
  slug: string;
  url: string;
  title: string;
  description: string | null;
  created_dt: string;
  start_dt: string;
  end_dt: string | null;
  status: string;
}

/**Contains common fields between a form element. */
interface APIElement {
  id: number;
  form: number;
  seq_no: number;
}

/**Interface for a HTML component. */
interface APIHTMLComponent extends APIElement {
  html: string;
}

/**Interface for a form question. */
interface APIFormQuestion extends APIElement {
  field_type: string;
  question: string;
  description: string;
  required: boolean;
  choices: string;
  related_question: number | null;
}

/**Interface for the form element type. */
interface APIElementType {
  id: string;
  app_label: string;
  model: string;
}

/**Interface for a form element. */
interface APIFormElement {
  id: number;
  element: APIHTMLComponent | APIFormQuestion;
  element_type: APIElementType;
  element_id: number;
  seq_no: number;
  form: number;
}

/**Interfaces represents an API response containing form details. The details
 * include the form elements belonging to a form.
 */
export interface APIFormDetail extends APIForm {
  form_elements: APIFormElement[];
}

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
 * Converts an API HTML component to an HTML component.
 * @param data - The API HTML component.
 * @returns - The HTML component.
 */
const HTMLComponentFormAPI = (data: APIHTMLComponent): HTMLComponent => {
  return {
    id: data.id,
    seqNo: data.seq_no,
    html: data.html,
  };
};

/**
 * Converts an API form question to a form question.
 * @param data - The API form question.
 * @returns - The form question.
 */
const formQuestionFromAPI = (data: APIFormQuestion): FormQuestion => {
  return {
    id: data.id,
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
      element = HTMLComponentFormAPI(data.element as APIHTMLComponent);
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
