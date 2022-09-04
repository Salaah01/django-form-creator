import React, { Component } from "react";
import {
  formElementFromAPI,
  formElementToAPI,
  HTMLComponentFromAPI,
} from "../../adapters";
import getAPIEndpoint from "../../apiEndpoints";
import {
  APIElementOptions,
  APIFormElement,
  APIFormQuestion,
  APIHTMLComponent,
  ElementOptions,
  FormElement,
  FormQuestion,
  HTMLComponent,
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

  /**Returns as JSON representation of this object. */
  asJSON = (): APIFormElement => {
    return formElementToAPI(this.state);
  };

  /**URL to submit the post request to. */
  postURL = (): string => {
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

  /**URL to submit the put request to. */
  abstract putURL(): string;

  /**URL to submit the delete request to. */
  deleteURL = (): string => {
    return this.putURL();
  };

  /**On submit handler. Typically, this should send the data to the URL and
   * call a function to update local redux state.
   */
  onSubmit = () => {
    if (this.state.element.id) {
      this.sendPutRequest();
    } else {
      this.sendPostRequest();
    }
  };

  /**Sends a post request for a new element. */
  sendPostRequest = () => {
    fetch(this.postURL(), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(this.asJSON()),
    })
      .then((res) => res.json())
      .then((data: APIFormElement) => {
        const processedData = formElementFromAPI(data);
        this.setState({
          id: processedData.element.id,
          element: processedData.element,
          elementType: processedData.elementType,
          formChangedSinceSubmit: false,
        });
      });
  };

  /**Function to covert API response data to a form element. */
  abstract elementFromAPI: (data: any) => ElementOptions;

  /**Sends a put request to update an element. */
  sendPutRequest = () => {
    fetch(this.putURL(), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(this.asJSON().element),
    })
      .then((res) => res.json())
      .then((data: APIElementOptions) => {
        const processedData = this.elementFromAPI(data);
        this.setState({
          id: processedData.id,
          element: processedData,
          formChangedSinceSubmit: false,
        });
      });
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
