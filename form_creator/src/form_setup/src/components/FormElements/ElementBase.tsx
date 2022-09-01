import React, { Component } from "react";
import { formElementToAPI } from "../../adapters";
import getAPIEndpoint from "../../apiEndpoints";
import {
  APIElementOptions,
  APIFormElement,
  ElementOptions,
  FormElement,
} from "../../interfaces";
import classes from "./ElementBase.module.scss";

export interface State extends FormElement {
  formChangedSinceSubmit: boolean;
}

/**Represents an abstract bass class for a form element. */
abstract class ElementBase extends Component<any> {
  abstract state: State;

  /**Determine of the fields on the component are completed
   * (all required fields) complete.
   */
  abstract isComplete(): boolean;

  /**Initializes the state of this element. */
  componentDidMount = (): void => {
    if (this.props.element) {
      this.setState({
        element: this.props.element,
        form: this.props.form.id,
      });
    } else {
      this.setState({
        element: { ...this.state.element, form: this.props.form_id },
      });
    }
  };

  /**URL to submit the form to. */
  submitURL = (): string => {
    const element = this.state.element as ElementOptions;
    if (element.id) {
      return getAPIEndpoint(
        "form-element-detail",
        "url-form-element-detail",
        element.id
      );
    } else {
      return getAPIEndpoint("form-element-list", "url-form-element-list");
    }
  };

  /**On submit handler. Typically, this should send the data to the URL and
   * call a function to update local redux state.
   */
  onSubmit = () => {
    const url = this.submitURL();
    const data = this.asJSON();
    fetch(url, {
      method: this.state.element.id ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data: APIElementOptions) => {
        console.log(data);
      });
  };

  /**Returns as JSON representation of this object. */
  asJSON = (): APIFormElement => {
    console.log(this.state);
    return formElementToAPI(this.state);
  };

  /**A wrapper that applies styles to the rendered component. */
  ElementWrapper: React.FC<any> = ({ children }) => {
    return (
      <div className={classes.Container} onBlur={this.onFormBlur}>
        {children}
      </div>
    );
  };

  onFormBlur = (_: React.ChangeEvent) => {
    if (!this.isComplete()) {
      return;
    }
    if (!this.state.formChangedSinceSubmit) {
      return;
    }
    this.onSubmit();
  };
}

export default ElementBase;
