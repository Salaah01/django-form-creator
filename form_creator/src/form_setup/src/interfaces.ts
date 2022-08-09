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


export interface HTMLComponent {
  seqNo: number;
  html: string;
}

export interface FormQuestion {
  seqNo: number;
  fieldType: string;
  question: string;
  description: string;
  required: boolean;
  choices?: string[];
}



export interface ElementType {
  id?: string;
  appLabel?: string;
  model?: string;
}

export interface Form {
  editorOptions: { id: string, name: string }[],
  editors?: { id: string, name: string }[],
  title: string,
  slug?: string,
  description?: string,
  startDt?: string,
  endDt?: string,
  status?: string,
}