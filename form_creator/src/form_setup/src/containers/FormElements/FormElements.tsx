import React, { Component } from "react";
import Button from "react-bootstrap/Button";
import { connect } from "react-redux";
import {
  ConnectState,
  FormElement as IFormElement,
  ElementType,
} from "../../interfaces";
import classes from "./FormElements.module.scss";
import * as elementTypes from "../../elementTypes";
import HTMLComponentElem from "../../components/FormElements/HTMLComponent";
import FormQuestionElem from "../../components/FormElements/FormQuestion";

interface Props {
  form_id: number;
  formElements: IFormElement[];
}

const getFormElement = (elementType: ElementType) => {
  const { appLabel, model } = elementType;

  switch ({ appLabel, model }) {
    case {
      appLabel: elementTypes.HTML_COMPONENT,
      model: elementTypes.HTML_COMPONENT,
    }:
      return HTMLComponentElem;
    default:
      throw new Error(`No form element found for ${elementType}`);
  }
};

const AddElementFactory = (elementType: ElementType) => {
  switch (elementType) {
    case elementTypes.HTML_COMPONENT:
      return HTMLComponentElem;
    case elementTypes.FORM_QUESTION:
      return FormQuestionElem;
    default:
      throw new Error(`No form element for ${elementType}`);
  }
};

class FormElements extends Component<Props> {
  state = {
    additionalElements: [],
  };

  ComponentPicker = () => {
    return (
      <div className={classes.ComponentPicker}>
        <h5>Add component</h5>
        <div className={classes.ComponentPicker__Buttons}>
          <Button
            variant="primary"
            className={classes.ComponentPicker__Button}
            onClick={() => this.addNewElement(elementTypes.HTML_COMPONENT)}
          >
            Add HTML Component
          </Button>
          <Button
            variant="primary"
            className={classes.ComponentPicker__Button}
            onClick={() => this.addNewElement(elementTypes.FORM_QUESTION)}
          >
            Add Form Question
          </Button>
        </div>
      </div>
    );
  };

  addNewElement = (elementType: ElementType) => {
    const FormElement = AddElementFactory(elementType);
    const numElements = this.state.additionalElements.length;
    const key = `additional-element-${numElements}`;
    this.setState({
      additionalElements: [
        ...this.state.additionalElements,
        <FormElement key={key} form_id={this.props.form_id} />,
      ],
    });
  };

  BuildArea = () => {
    const elements = [];
    for (let i = 0; i < this.props.formElements.length; i++) {
      const Element = getFormElement(this.props.formElements[i].elementType);
      elements.push(
        <Element key={i} formElement={this.props.formElements[i]} />
      );
    }

    for (let i = 0; i < this.state.additionalElements.length; i++) {
      elements.push(this.state.additionalElements[i]);
    }

    return <div className={classes.BuildArea}>{elements}</div>;
  };

  render() {
    return (
      <div>
        <h1>Form Elements</h1>
        <div className={classes.MainContainer}>
          <this.BuildArea />
          <this.ComponentPicker />
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    form_id: state.formSetup.form.id,
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(FormElements);
