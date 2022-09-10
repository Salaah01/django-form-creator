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
import { formDetailFromAPI, formDetailToAPI } from "./adapters";
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
  componentDidMount() {
    const formIDElem = document.querySelector(
      "#form-id"
    ) as HTMLInputElement | null;
    if (formIDElem && formIDElem.value) {
      const formID = parseInt(formIDElem.value);
      this.loadFormDetails(formID);
    }
  }

  /**If the user has provided a formID, then function will load the form
   * details data and store it in the redux store.
   * @param formID - The ID of the form to load
   */
  loadFormDetails = (formID: number) => {
    const url = getAPIEndpoint("form-detail", "api-form-detail", formID);
    fetch(url)
      .then((res) => {
        console.log(res);
        return res.json();
      })
      .then((data: interfaces.APIFormDetail) => {
        const formDetail = formDetailFromAPI(data);
        this.props.updateFormDetails(formDetail);
      });
  };

  detailsFormOnClickHandler = (event: Event) => {
    event.preventDefault();

    let apiEndpoint: string;
    let method: string;

    if (this.props.form.id) {
      apiEndpoint = getAPIEndpoint(
        "form-detail",
        "api-form-detail",
        this.props.form.id
      );
      method = "PUT";
    } else {
      apiEndpoint = getAPIEndpoint("form-detail", "api-form-detail");
      method = "POST";
    }

    const data = formDetailToAPI({
      form: this.props.form,
      // Set to an empty array as the endpoint is currently unable to handle
      // form elements. This is handled separately.
      formElements: [],
    });

    console.log(data);

    fetch(apiEndpoint, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() || "",
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data: interfaces.APIFormDetail) => {
        console.log(data);
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

    return (
      <div className="container mt-5">
        <Form>{FormContent}</Form>
      </div>
    );
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
