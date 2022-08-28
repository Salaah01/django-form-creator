import React, { Component } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { connect } from "react-redux";
import {
  ConnectState,
  FormElement as IFormElement,
  ElementType,
} from "../../interfaces";
import HTMLComponentElem from "../../components/FormElements/HTMLComponent";

interface Props {
  formElements: IFormElement[];
}

const getFormElement = (elementType: ElementType) => {
  const { appLabel, model } = elementType;
  if (appLabel === "form_creator" && model === "formquestion") {
    return HTMLComponentElem;
  }
  throw new Error(`No form element for ${elementType}`);
};

class FormElements extends Component<Props> {
  ComponentPicker = () => {
    return (
      <div>
        <h2>Elements</h2>
        <div className="flex">
          <Button variant="primary">Add HTML Component</Button>
          <Button variant="primary">Add Form Question</Button>
        </div>
      </div>
    );
  };

  BuildArea = () => {
    const elements = [];
    for (let i = 0; i < this.props.formElements.length; i++) {
      const Element = getFormElement(this.props.formElements[i].elementType);
      elements.push(<Element key={i} formElement={this.props.formElements[i]} />);
    }
  };

  render() {
    return (
      <div>
        <h1>Form Elements</h1>
        <div>
          <this.ComponentPicker />
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(FormElements);
