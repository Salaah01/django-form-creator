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
import * as actions from "../../store/actions";
import HTMLComponentElem from "../../components/FormElements/HTMLComponent";
import FormQuestionElem from "../../components/FormElements/FormQuestion";

interface Props {
  formId: number;
  formElements: IFormElement[];
  addBlankFormElement: any;
}

const getFormElement = (elementType: ElementType) => {
  const { appLabel, model } = elementType;

  const elementTypeComponentMap: [ElementType, any][] = [
    [elementTypes.HTML_COMPONENT, HTMLComponentElem],
    [elementTypes.FORM_QUESTION, FormQuestionElem],
  ];

  for (const elementTypeComponent of elementTypeComponentMap) {
    const elemType = elementTypeComponent[0] as ElementType;

    if (elemType.appLabel === appLabel && elemType.model === model) {
      return elementTypeComponent[1];
    }
  }

  throw new Error(`No form element found for ${elementType}`);
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
            onClick={() =>
              this.props.addBlankFormElement(
                elementTypes.HTML_COMPONENT,
                this.props.formId
              )
            }
          >
            Add HTML Component
          </Button>
          <Button
            variant="primary"
            className={classes.ComponentPicker__Button}
            onClick={() =>
              this.props.addBlankFormElement(
                elementTypes.FORM_QUESTION,
                this.props.formId
              )
            }
          >
            Add Form Question
          </Button>
        </div>
      </div>
    );
  };

  addNewElement = (elementType: ElementType) => {
    this.props.addBlankFormElement(elementType, this.props.formId);
  };

  BuildArea = () => {
    const elements = [];
    for (let i = 0; i < this.props.formElements.length; i++) {
      const Element = getFormElement(this.props.formElements[i].elementType);
      elements.push(
        <Element
          key={i}
          formElement={this.props.formElements[i]}
          formId={this.props.formId}
        />
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
    formId: state.formSetup.form.id,
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    addFormElement: (formElement: IFormElement) =>
      dispatch(actions.addFormElement(formElement)),
    addBlankFormElement: (elementType: ElementType, formId: number) =>
      dispatch(actions.addBlankFormElement(elementType, formId)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FormElements);
