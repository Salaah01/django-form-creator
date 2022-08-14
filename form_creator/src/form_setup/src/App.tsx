import React from 'react';
import { connect } from 'react-redux';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Form from "react-bootstrap/Form";
import DetailsForm from './containers/DetailsForm/DetailsForm';
import FormElements from './containers/FormElements/FormElements';
import { ConnectState } from './interfaces';

function App() {
  return (
    <Form>
      <DetailsForm />
      <FormElements />
    </Form>
  );
}


const mapStateToProps = (state: ConnectState) => {
  return {
    form: state.formSetup.form
  }
}

const mapDispatchToProps = (dispatch: any) => {
  return {}
}

export default connect(mapStateToProps, mapDispatchToProps)(App);