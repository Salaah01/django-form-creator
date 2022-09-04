import React, { ChangeEvent } from "react";
import ElementBase, { State } from "./ElementBase";
import Form from "react-bootstrap/Form";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { FORM_QUESTION } from "../../elementTypes";
import { FormElement } from "../../interfaces";
import getAPIEndpoint from "../../apiEndpoints";
import { formQuestionFromAPI } from "../../adapters";

const fieldTypeOptions = [
  { value: "text", label: "Text" },
  { value: "textarea", label: "Textarea" },
  { value: "email", label: "Email" },
  { value: "integer", label: "Integer" },
  { value: "decimal", label: "Decimal" },
  { value: "float", label: "Float" },
  { value: "boolean", label: "Boolean" },
  { value: "date", label: "Date" },
  { value: "datetime", label: "Datetime" },
  { value: "time", label: "Time" },
  { value: "url", label: "URL" },
  { value: "choice", label: "Choice" },
  { value: "multiple_choice", label: "Multiple Choice" },
];

const choiceTypeOptions = ["choice", "multiple_choice"];

class FormQuestionElem extends ElementBase {
  state = {
    id: null,
    element: {
      fieldType: "",
      question: "",
      description: "",
      required: true,
      choices: [],
    },
    elementType: FORM_QUESTION,
    formChangedSinceSubmit: false,
  };

  isComplete = (): boolean => {
    const requiredFields = ["fieldType", "question"];
    const element = this.state.element as { [key: string]: any };

    if (requiredFields.some((field) => !element[field])) {
      return false;
    }

    if (this.choiceTypeSelected()) {
      return Boolean(element.choices.length);
    }

    return true;
  };

  /**Indicate whether the selected field type is of a choice type. */
  choiceTypeSelected = (): boolean => {
    return choiceTypeOptions.includes(this.state.element.fieldType);
  };

  /**
   * Handler for when a user changes a form field value.
   * @param event - The event that triggered the change.
   * @param field - The field that was changed.
   */
  onChangeFormValue = (event: ChangeEvent, field: string) => {
    this.setState((prevState: Readonly<State>) => ({
      ...prevState,
      element: {
        ...prevState.element,
        [field]: (event.target as HTMLInputElement).value,
      },
      formChangedSinceSubmit: true,
    }));
  };

  /**
   * Handler for when a user makes a change to the choices field.
   * @param event - The event that triggered the change.
   */
  onChangeChoices = (event: ChangeEvent) => {
    this.setState((prevState: Readonly<State>) => ({
      ...prevState,
      element: {
        ...prevState.element,
        choices: (event.target as HTMLInputElement).value.split("|"),
      },
      formChangedSinceSubmit: true,
    }));
  };

  /**Event handler for updating the form description.
   * @param event - The event that triggered the change.
   * @param editor - The editor that was changed.
   */
  onChangeDescription = (_: ChangeEvent, editor: { getData: () => any }) => {
    const data = editor.getData();
    this.setState((prevState: Readonly<State>) => ({
      ...prevState,
      element: {
        ...prevState.element,
        description: data,
      },
      formChangedSinceSubmit: true,
    }));
  };

  elementFromAPI = formQuestionFromAPI;

  putURL = (): string => {
    return getAPIEndpoint(
      "form-element-form-question",
      "form-element-form-question-url",
      this.state.id,
    );
  };

  render() {
    return (
      <this.ElementWrapper>
        <Form.Group controlId="fieldType">
          <Form.Label>Field Type</Form.Label>
          <Form.Select
            aria-label="Field type"
            onChange={(event) => this.onChangeFormValue(event, "fieldType")}
          >
            <option>Select a field type</option>
            {fieldTypeOptions.map(({ value, label }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Form.Group controlId="question">
          <Form.Label>Question</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter question"
            value={this.state.element.question}
            onChange={(event) => this.onChangeFormValue(event, "question")}
          />
        </Form.Group>

        <Form.Group controlId="description">
          <Form.Label>Description</Form.Label>
          <CKEditor
            editor={ClassicEditor}
            data={this.state.element.description}
            onChange={this.onChangeDescription}
          />
        </Form.Group>

        <Form.Group controlId="required">
          <Form.Check
            type="checkbox"
            label="Required"
            checked={this.state.element.required}
            onChange={(event) => this.onChangeFormValue(event, "required")}
          />
        </Form.Group>

        <Form.Group controlId="choices">
          <Form.Label>Choices</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter choices (separated by '|')"
            value={this.state.element.choices.join("|")}
            onChange={(event) => this.onChangeChoices(event)}
            disabled={!this.choiceTypeSelected()}
          />
        </Form.Group>
      </this.ElementWrapper>
    );
  }
}

export default FormQuestionElem;
