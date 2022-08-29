import React, { Component } from "react";
import { FormElement } from "../../interfaces";
import classes from "./ElementBase.module.scss";

export interface State extends FormElement {}

/**Represents an abstract bass class for a form element. */
abstract class ElementBase extends Component<any> {
  abstract state: State;

  /**Initializes the state of this element. */
  componentDidMount = (): void => {
    if (this.props.element) {
      this.setState({
        element: this.props.element,
        form: this.props.form.id,
      });
    }
  };
  /**Returns as JSON representation of this object. */
  asJSON = (): FormElement => {
    return {
      element: this.state.element,
      elementType: this.state.elementType,
    };
  }

  // ElementWrapper = (children: React.ReactElement) => {
  //   return <div className={classes.Container}>{children}</div>
  // }
  ElementWrapper: React.FC<any> = ({ children }) => {
    return <div className={classes.Container}>{children}</div>;
  }
}

export default ElementBase;
