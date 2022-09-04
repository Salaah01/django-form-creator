import React from "react";
import { connect } from "react-redux";
import "bootstrap/dist/css/bootstrap.min.css";
import Form from "react-bootstrap/Form";
import getAPIEndpoint from "./apiEndpoints";
import DetailsForm from "./containers/DetailsForm/DetailsForm";
import FormElements from "./containers/FormElements/FormElements";
import * as screens from "./screens";
import * as interfaces from "./interfaces";
import * as actions from "./store/actions";
import { formDetailFromAPI } from "./adapters";
import { getCSRFToken, valueOrNull } from "./utils";

interface Props {
  httpMethod: interfaces.HttpMethod;
  screen: screens.ScreenOption;
  form: interfaces.Form;
  formElements: interfaces.FormElement[];
  updateFormDetails: (formDetails: interfaces.FormDetail) => void;
  updateScreen: (screen: screens.ScreenOption) => void;
}
class App extends React.Component<Props> {
  detailsFormOnClickHandler = (event: Event) => {
    event.preventDefault();
    const apiEndpoint = getAPIEndpoint("form-list", "api-form-list");
    const data = {
      title: valueOrNull(this.props.form.title),
      description: valueOrNull(this.props.form.description),
      start_dt: valueOrNull(this.props.form.startDt),
      end_dt: valueOrNull(this.props.form.endDt),
      status: valueOrNull(this.props.form.status),
      form_elements: this.props.formElements,
    };
    fetch(apiEndpoint, {
      method: this.props.httpMethod,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() || "",
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data: interfaces.APIFormDetail) => {
        this.props.updateFormDetails(formDetailFromAPI(data));
        this.props.updateScreen(screens.FORM_ELEMENTS);
      });
  };

  render() {
    let FormContent;
    switch (this.props.screen) {
      case screens.FORM_DETAILS:
        FormContent = <DetailsForm onSubmit={this.detailsFormOnClickHandler} />;
        break;
      case screens.FORM_ELEMENTS:
        FormContent = <FormElements />;
        break;
      default:
        FormContent = <div>Error</div>;
    }

    return <div className="container mt-5"><Form>{FormContent}</Form></div>;
  }
}

const mapStateToProps = (state: interfaces.ConnectState) => {
  return {
    screen: state.formSetup.screen,
    form: state.formSetup.form,
    httpMethod: state.formSetup.httpMethod,
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    updateFormDetails: (formDetails: interfaces.FormDetail) =>
      dispatch(actions.updateFormDetails(formDetails)),
    updateScreen: (screen: screens.ScreenOption) =>
      dispatch(actions.updateScreen(screen)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);