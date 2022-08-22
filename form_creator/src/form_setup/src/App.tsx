import React from "react";
import { connect } from "react-redux";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Form from "react-bootstrap/Form";
import getAPIEndpoint from "./apiEndpoints";
import DetailsForm from "./containers/DetailsForm/DetailsForm";
import FormElements from "./containers/FormElements/FormElements";
import * as screens from "./screens";
import * as interfaces from "./interfaces";
import { getCSRFToken, valueOrNull } from "./utils";

interface AppProps {
  screen: screens.ScreenOption;
  form: interfaces.Form;
  formElements: interfaces.FormElement[];
}
class App extends React.Component<AppProps> {
  detailsFormOnClickHandler = (event: Event) => {
    console.log(1);

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
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() || "",
      },
      body: JSON.stringify(data),
    }).then((res) => console.log(res));
  };

  render() {
    if (this.props.screen === screens.FORM_DETAILS) {
      return (
        <Form>
          <DetailsForm onSubmit={this.detailsFormOnClickHandler} />
        </Form>
      );
    } else {
      return (
        <Form>
          <FormElements />
        </Form>
      );
    }
  }
}

const mapStateToProps = (state: interfaces.ConnectState) => {
  return {
    screen: state.formSetup.screen,
    form: state.formSetup.form,
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
