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
  seqNo: number;
}

/**Interface for a HTML component form element. */
export interface HTMLComponent extends Element {
  html: string;
}

/**Interface for a form question form element. */
export interface FormQuestion extends Element {
  fieldType: string;
  question: string;
  description: string;
  required: boolean;
  choices?: string[];
  relatedQuestion?: number|null;
}

/**Interface for element type. Contains information which can identify what
 * type of element is being accessed.
 */
export interface ElementType {
  id?: string;
  appLabel?: string;
  model?: string;
}

/**Interface for a form element. */
export interface FormElement {
  element: HTMLComponent | FormQuestion;
  elementType: ElementType;
}

/**Interface for a form. */
export interface Form {
  id?: number;
  editorOptions?: { id: string; name: string }[];
  editors?: { id: string; name: string }[];
  title: string;
  slug?: string;
  description?: string;
  startDt?: string;
  endDt?: string;
  status?: string;
}

/**Interface for a complete set of form details which contains the form itself
 * as well as the form elements.
 */
export interface FormDetail {
  form: Form;
  formElements: FormElement[];
}
