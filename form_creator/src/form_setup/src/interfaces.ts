/**Shared interfaces. */

export interface ConnectState {
  [key: string]: any;
}

/**Interface for an action with unknown properties. */
export interface AnyPropsObj {
  [key: string]: any;
}

/**Interface for a reducer. */
export interface ReducerAction {
  type: string;
  [x: string]: any;
}

/**Supported HTTP methods */
export type HttpMethod = "POST" | "PUT";

/**Common fields in an element. */
interface Element {
  id?: number;
  seqNo?: number;
  form?: number;
}

/**Contains common fields between a form element. */
interface APIElement {
  id?: number;
  form: number;
  seq_no?: number;
}

/**Interface for a HTML component form element. */
export interface HTMLComponent extends Element {
  html: string;
}

/**Interface for a HTML component. */
export interface APIHTMLComponent extends APIElement {
  html: string;
}

/**Interface for a form question form element. */
export interface FormQuestion extends Element {
  fieldType: string;
  question: string;
  description: string;
  required: boolean;
  choices?: string[];
  relatedQuestion?: number | null;
}

/**Interface for a form question. */
export interface APIFormQuestion extends APIElement {
  field_type: string;
  question: string;
  description: string;
  required: boolean;
  choices: string;
  related_question?: number | null;
}

export type ElementOptions = HTMLComponent | FormQuestion;
export type APIElementOptions = APIHTMLComponent | APIFormQuestion;

/**Interface for element type. Contains information which can identify what
 * type of element is being accessed.
 */
export interface ElementType {
  id?: string;
  appLabel?: string;
  model?: string;
}

/**Interface for the form element type. */
export interface APIElementType {
  id?: string;
  app_label: string;
  model: string;
}

/**Interface for a form element. */
export interface FormElement {
  element: ElementOptions;
  elementType: ElementType;
}

/**Interface for a form element. */
export interface APIFormElement {
  id?: number;
  element: APIHTMLComponent | APIFormQuestion;
  element_type: APIElementType;
  element_id?: number;
  seq_no?: number;
  form: number;
}

/**Interface for a form. */
export interface Form {
  id?: number;
  editorOptions?: { id: string; name: string }[];
  editors?: { id: string; name: string }[];
  title: string;
  slug?: string;
  description?: string;
  startDt?: Date|string;
  endDt?: Date|string;
  status?: string;
}

/**Interface for the form details part of an API. */
export interface APIForm {
  id?: number;
  slug?: string;
  url?: string;
  title: string;
  description: string | null;
  created_dt?: string;
  start_dt: string;
  end_dt: string | null;
  status: string;
}

/**Interface for a complete set of form details which contains the form itself
 * as well as the form elements.
 */
export interface FormDetail {
  form: Form;
  formElements: FormElement[];
}

/**Interfaces represents an API response containing form details. The details
 * include the form elements belonging to a form.
 */
export interface APIFormDetail extends APIForm {
  form_elements: APIFormElement[];
}
