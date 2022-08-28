/**Contains element types (dictionary representation of Django's ContentType). */

import { ElementType } from "./interfaces";

const APP_LABEL = "form_creator";

export const HTML_COMPONENT: ElementType = {
  appLabel: APP_LABEL,
  model: "htmlcomponent",
};

export const FORM_QUESTION: ElementType = {
  appLabel: APP_LABEL,
  model: "formquestion",
};
